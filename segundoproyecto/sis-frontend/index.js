import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import CsvUploader from '../components/CsvUploader.vue'; // Importar el componente

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/decision-tree',
    name: 'DecisionTree',
    component: arbol
  },
  {
    path: '/clustering',
    name: 'Clustering',
    component: CsvUploader // Este componente se reemplazará con el correcto más tarde
  },
  {
    path: '/perceptron',
    name: 'Perceptron',
    component: CsvUploader // Este componente se reemplazará con el correcto más tarde
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
