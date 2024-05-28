<template>
  <div class="relative flex flex-col items-center justify-center min-h-screen bg-gray-100 p-8 bg-cover bg-center" style="background-image: url('https://r4.wallpaperflare.com/wallpaper/527/757/70/aesthetic-neon-wallpaper-0f0ae73eba21fd1c1d95d0b498beb0d0.jpg');">
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
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKmkNey4cUdmHoo8dvCmmV8_kyN_GHJU-v6A&s" alt="Imagen de Esquina" class="absolute top-4 right-4 w-16 h-16 rounded-full shadow-lg cursor-pointer" @click="showModal = true">
    
    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div class="bg-white rounded-lg p-6 relative max-w-lg w-full mx-4">
        <button @click="showModal = false" class="absolute top-2 right-2 text-gray-500 hover:text-gray-700">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
        <div class="text-center">
          <h2 class="text-xl font-bold text-gray-700 mb-4">Descripción del Proyecto</h2>
          <p class="text-gray-600 mb-2">Este proyecto está orientado a analizar datos utilizando tres métodos diferentes:</p>
          <ul class="list-disc list-inside text-gray-600">
            <li><strong>Árboles de Decisión:</strong> Crea y visualiza árboles de decisión para análisis predictivo.</li>
            <li><strong>Clustering:</strong> Agrupa datos similares usando técnicas de clustering.</li>
            <li><strong>Perceptrón:</strong> Entrena y evalúa modelos de perceptrón multicapa.</li>
          </ul>
        </div>
      </div>
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
      currentView: '',
      showModal: false
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
