<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-8">
    <h1 class="text-2xl font-bold mb-8">Página Principal</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <button @click="currentView = 'decision-tree'" class="bg-blue-500 text-white font-bold py-4 px-8 rounded hover:bg-blue-600 transition-colors text-center">
        Árboles de Decisión
      </button>
      <button @click="currentView = 'clustering'" class="bg-blue-500 text-white font-bold py-4 px-8 rounded hover:bg-blue-600 transition-colors text-center">
        Clustering
      </button>
      <button @click="currentView = 'perceptron'" class="bg-blue-500 text-white font-bold py-4 px-8 rounded hover:bg-blue-600 transition-colors text-center">
        Perceptrón
      </button>
    </div>
    <div class="mt-8 w-full">
      <component :is="currentViewComponent" />
    </div>
  </div>
</template>

<script>
import PerceptronUploader from './components/perceptron.vue';
import Arbol from './components/arbol.vue';
import Clustering from './components/clustering.vue';
import Perceptron from './components/perceptron.vue';

export default {
  name: 'App',
  components: {
    Arbol,
    Clustering,
    Perceptron
  },
  data() {
    return {
      currentView: ''
    };
  },
  computed: {
    currentViewComponent() {
      switch (this.currentView) {
        case 'decision-tree':
          return 'arbol';
        case 'clustering':
          return 'clustering';
        case 'perceptron':
          return 'perceptron';
        default:
          return {
            template: '<div>Seleccione una opción para comenzar</div>'
          };
      }
    }
  }
};
</script>

<style scoped>
/* Añadir estilos adicionales si es necesario */
</style>
