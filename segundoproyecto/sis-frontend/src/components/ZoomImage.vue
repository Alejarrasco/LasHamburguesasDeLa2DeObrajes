<template>
    <div class="zoom-container" @click="toggleZoom">
      <img 
        :src="src" 
        :style="imageStyles" 
        ref="imageRef"
        class="zoom-image"
        @load="updateImageSize"
      />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, onMounted } from 'vue';
  
  export default defineComponent({
    name: 'ZoomImage',
    props: {
      src: {
        type: String,
        required: true
      }
    },
    setup(props) {
      const imageRef = ref<HTMLImageElement | null>(null);
      const scale = ref(1);
      const originX = ref(0);
      const originY = ref(0);
  
      const updateImageSize = () => {
        if (imageRef.value) {
          scale.value = 1;  // Reset scale on image load
        }
      };
  
      const toggleZoom = (event: MouseEvent) => {
        const rect = imageRef.value?.getBoundingClientRect();
        if (!rect) return;
  
        const offsetX = event.clientX - rect.left;
        const offsetY = event.clientY - rect.top;
  
        if (scale.value === 1) {
          // Zoom in
          scale.value = 2;  // Or any desired zoom level
          originX.value = offsetX / scale.value;
          originY.value = offsetY / scale.value;
        } else {
          // Zoom out
          scale.value = 1;
          originX.value = 0;
          originY.value = 0;
        }
      };
  
      const imageStyles = computed(() => ({
        transform: `scale(${scale.value})`,
        transformOrigin: `${originX.value}px ${originY.value}px`,
        transition: 'transform 0.4s ease'
      }));
  
      onMounted(updateImageSize);
  
      return {
        imageRef,
        imageStyles,
        toggleZoom,
        updateImageSize
      };
    }
  });
  </script>
  
  <style scoped>
  .zoom-container {
    width: 100%;
    height: 100%;
    overflow: hidden;
    position: relative;
    cursor: zoom-in;
  }
  .zoom-image {
    display: block;
    max-width: 100%;
  }
  </style>
  