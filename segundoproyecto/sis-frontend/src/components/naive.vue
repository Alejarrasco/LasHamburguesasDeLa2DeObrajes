<template>
    <div class="flex flex-col items-center justify-center p-8 bg-white rounded-lg shadow-xl">
      <label
        for="file-upload"
        class="flex items-center justify-center cursor-pointer bg-blue-500 text-white font-bold py-3 px-6 rounded hover:bg-blue-600 transition-colors"
      >
        <DocumentIcon class="h-6 w-6 text-white mr-2"/>
        Subir archivo CSV
      </label>
      <input id="file-upload" type="file" @change="handleFileUpload" accept=".csv" class="hidden"/>
  
      <div v-if="columns.length > 0" class="mt-4">
        <select v-model="selectedColumn" class="border border-gray-300 rounded p-2">
          <option disabled value="">Seleccione una columna para el target</option>
          <option v-for="column in columns" :key="column" :value="column">
            {{ column }}
          </option>
        </select>
      </div>
  
      <button v-if="selectedColumn" @click="submitData" class="mt-4 bg-green-500 text-white font-bold py-2 px-4 rounded hover:bg-green-600 transition-colors">
        Subir datos
      </button>
  
      <div v-if="isLoading" class="mt-4 flex items-center justify-center">
  <img src="https://64.media.tumblr.com/be3ce7e4703c3e208790c3ed4249db99/0c7447b1cf7154b1-c4/s640x960/14fd1548c126d24b96e4731647c868ed26f1fdfe.gif" alt="Cargando..." class="h-16 w-16">
  </div>
  
      <div v-if="report" class="mt-4 w-full">
        <pre>{{ report }}</pre>
      </div>
  
      <div v-if="errorMessage" class="mt-4 text-red-500">
        {{ errorMessage }}
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  import Papa from 'papaparse';
  import axios from 'axios';
  import { DocumentIcon } from '@heroicons/vue/24/solid';
  
  export default defineComponent({
    name: 'NaiveBayesUploader',
    components: {
      DocumentIcon
    },
    setup() {
      const columns = ref<string[]>([]);
      const selectedColumn = ref('');
      const fileRef = ref<File | null>(null);
      const report = ref<string | null>(null);
      const isLoading = ref(false);
      const errorMessage = ref<string | null>(null);
  
      const handleFileUpload = (event: Event) => {
        const files = (event.target as HTMLInputElement).files;
        if (files && files[0]) {
          fileRef.value = files[0];
          Papa.parse(files[0], {
            complete: function(results) {
              if (results.meta && results.meta.fields) {
                columns.value = results.meta.fields;
              } else {
                console.error("CSV does not have headers or is incorrectly formatted.");
              }
            },
            header: true
          });
        }
      };
  
      const submitData = () => {
        if (fileRef.value && selectedColumn.value) {
          isLoading.value = true;
          errorMessage.value = null; // Reset error message
          const formData = new FormData();
          formData.append('file', fileRef.value);
          const url = `http://localhost:8000/naive-bayes/?target_column=${encodeURIComponent(selectedColumn.value)}`;
  
          axios.post(url, formData)
          .then(response => {
            report.value = atob(response.data.report);
          })
          .catch(error => {
            console.error('Error uploading file:', error);
            if (error.response && error.response.data && error.response.data.detail) {
              errorMessage.value = error.response.data.detail;
            } else {
              errorMessage.value = 'Error al subir el archivo. Ver consola para detalles.';
            }
          })
          .finally(() => {
            isLoading.value = false;
          });
        } else {
          alert('Archivo o columna no seleccionados correctamente.');
        }
      };
  
      return { columns, selectedColumn, handleFileUpload, submitData, report, isLoading, errorMessage };
    }
  });
  </script>
  
  <style scoped>
  /* Añadir estilos adicionales si es necesario */
  </style>
  