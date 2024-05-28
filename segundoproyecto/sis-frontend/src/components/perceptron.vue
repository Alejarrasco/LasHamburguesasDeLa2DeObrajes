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

    <div v-if="selectedColumn" class="mt-4">
  <label for="hidden-layers" class="block text-gray-700 font-bold mb-2">Dimensiones de las capas ocultas</label>
  <input id="hidden-layers" type="text" v-model="hiddenLayers" class="border border-gray-300 rounded p-2 w-full" placeholder="Capas ocultas (ej. 2,3,2)" />
</div>


    <button v-if="selectedColumn" @click="submitData" class="mt-4 bg-green-500 text-white font-bold py-2 px-4 rounded hover:bg-green-600 transition-colors">
      Subir datos
    </button>

    <div v-if="isLoading" class="mt-4 flex items-center justify-center">
  <img src="https://64.media.tumblr.com/be3ce7e4703c3e208790c3ed4249db99/0c7447b1cf7154b1-c4/s640x960/14fd1548c126d24b96e4731647c868ed26f1fdfe.gif" alt="Cargando..." class="h-16 w-16">
  </div>


    <div v-if="report" class="mt-4 w-full">
      <h3 class="font-bold">Reporte del Perceptrón Multicapa</h3>
      <pre>{{ report }}</pre>
    </div>

    <div v-if="confusionMatrixImage" class="mt-4 w-full">
      <h3 class="font-bold">Matriz de Confusión</h3>
      <img :src="confusionMatrixImage" alt="Confusion Matrix" class="max-w-full"/>
    </div>

    <div v-if="decisionBoundaryImage" class="mt-4 w-full">
      <h3 class="font-bold">Superficie de Decisión</h3>
      <img :src="decisionBoundaryImage" alt="Decision Boundary" class="max-w-full"/>
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
  name: 'PerceptronUploader',
  components: {
    DocumentIcon
  },
  setup() {
    const columns = ref<string[]>([]);
    const selectedColumn = ref('');
    const hiddenLayers = ref<string>('2,2');
    const fileRef = ref<File | null>(null);
    const report = ref<string | null>(null);
    const confusionMatrixImage = ref<string | null>(null);
    const decisionBoundaryImage = ref<string | null>(null);
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
        const url = `http://localhost:8000/multilayer-perceptron/?target_column=${encodeURIComponent(selectedColumn.value)}&hidden_layers=${hiddenLayers.value}`;

        axios.post(url, formData)
        .then(response => {
          report.value = atob(response.data.report);
          confusionMatrixImage.value = `data:image/png;base64,${response.data.confusion_matrix}`;
          if (response.data.decision_boundary) {
            decisionBoundaryImage.value = `data:image/png;base64,${response.data.decision_boundary}`;
          } else {
            decisionBoundaryImage.value = null;
          }
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

    return { columns, selectedColumn, hiddenLayers, fileRef, handleFileUpload, submitData, report, confusionMatrixImage, decisionBoundaryImage, isLoading, errorMessage };
  }
});
</script>

<style scoped>
/* Añadir estilos adicionales si es necesario */
</style>
