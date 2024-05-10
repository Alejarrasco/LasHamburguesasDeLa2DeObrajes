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

    <!-- Visualización de la imagen del árbol de decisiones -->
    <div v-if="decisionTreeImage" class="mt-4 w-full">
      <img :src="decisionTreeImage" alt="Árbol de Decisiones" class="w-full h-auto rounded shadow-md"/>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Papa from 'papaparse';
import axios from 'axios';
import { DocumentIcon } from '@heroicons/vue/24/solid';

export default defineComponent({
  name: 'CsvUploader',
  components: {
    DocumentIcon
  },
  setup() {
    const columns = ref<string[]>([]);
    const selectedColumn = ref('');
    const fileRef = ref<File | null>(null);
    const decisionTreeImage = ref<string | null>(null); // Para almacenar la URL de la imagen

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
        const formData = new FormData();
        formData.append('file', fileRef.value);
        const url = `http://localhost:8000/process_csv/?target_column=${encodeURIComponent(selectedColumn.value)}`;

        axios.post(url, formData)
        .then(response => {
          decisionTreeImage.value = `data:image/svg+xml;base64,${response.data.decision_tree}`;
        })
        .catch(error => {
          console.error('Error uploading file:', error);
          alert('Error al subir el archivo. Ver consola para detalles.');
        });
      } else {
        alert('Archivo o columna no seleccionados correctamente.');
      }
    };

    return { columns, selectedColumn, handleFileUpload, submitData, decisionTreeImage };
  }
});
</script>

<style scoped>
/* Añadir estilos adicionales si es necesario */
</style>
