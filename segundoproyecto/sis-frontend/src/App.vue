<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-8 bg-cover bg-center" style="background-image: url('https://r4.wallpaperflare.com/wallpaper/527/757/70/aesthetic-neon-wallpaper-0f0ae73eba21fd1c1d95d0b498beb0d0.jpg');">
    <h1 class="text-4xl font-bold mb-8 text-white">Herramientas de Análisis de Datos</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div @click="selectView('decision-tree')" :class="{'border-4 border-green-500': currentView === 'decision-tree'}" class="relative bg-white shadow-lg rounded-lg overflow-hidden transform hover:scale-105 transition-transform cursor-pointer">
        <div class="absolute inset-0 bg-cover bg-center opacity-50" style="background-image: url('/path/to/your/decision-tree.jpg');"></div>
        <div class="relative p-6 text-center">
          <h2 class="text-xl font-bold text-gray-700 mb-2">Árboles de Decisión</h2>
          <p class="text-gray-600">Crea y visualiza árboles de decisión para análisis predictivo.</p>
        </div>
      </div>
      <div @click="selectView('clustering')" :class="{'border-4 border-green-500': currentView === 'clustering'}" class="relative bg-white shadow-lg rounded-lg overflow-hidden transform hover:scale-105 transition-transform cursor-pointer">
        <div class="absolute inset-0 bg-cover bg-center opacity-50" style="background-image: url('/path/to/your/clustering.jpg');"></div>
        <div class="relative p-6 text-center">
          <h2 class="text-xl font-bold text-gray-700 mb-2">Clustering</h2>
          <p class="text-gray-600">Agrupa datos similares usando técnicas de clustering.</p>
        </div>
      </div>
      <div @click="selectView('perceptron')" :class="{'border-4 border-green-500': currentView === 'perceptron'}" class="relative bg-white shadow-lg rounded-lg overflow-hidden transform hover:scale-105 transition-transform cursor-pointer">
        <div class="absolute inset-0 bg-cover bg-center opacity-50" style="background-image: url('/path/to/your/perceptron.jpg');"></div>
        <div class="relative p-6 text-center">
          <h2 class="text-xl font-bold text-gray-700 mb-2">Perceptrón</h2>
          <p class="text-gray-600">Entrena y evalúa modelos de perceptrón multicapa.</p>
        </div>
      </div>
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
  methods: {
    selectView(view) {
      this.currentView = view;
    }
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
            template: '<div class="text-center text-gray-700">Seleccione una opción para comenzar</div>'
          };
      }
    }
  }
};
</script>

<style scoped>
/* Añadir estilos adicionales si es necesario */
</style>
