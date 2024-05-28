<template>
  <div class="zoom-container" 
       @mousedown="handleMouseDown" 
       @mouseup="stopDragging" 
       @mouseleave="stopDragging"
       @mousemove="onMouseMove">
    <img 
      :src="src" 
      :style="imageStyles" 
      ref="imageRef"
      class="zoom-image"
      @load="updateImageSize"
      @dblclick="resetZoom"
      @dragstart.prevent
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
    const containerRef = ref<HTMLDivElement | null>(null);
    const scale = ref(1);
    const originX = ref(50);
    const originY = ref(50);
    const isDragging = ref(false);
    const startX = ref(0);
    const startY = ref(0);
    const clickCount = ref(0);

    const updateImageSize = () => {
      if (imageRef.value) {
        scale.value = 1;  // Reset scale on image load
      }
    };

    const handleMouseDown = (event: MouseEvent) => {
      event.preventDefault(); // Prevent default dragging behavior
      clickCount.value++;

      if (clickCount.value === 1) {
        setTimeout(() => {
          if (clickCount.value === 1) {
            startDragging(event);
          }
          clickCount.value = 0;
        }, 200); // Espera 200ms para determinar si es un clic o doble clic
      }
    };

    const startDragging = (event: MouseEvent) => {
      isDragging.value = true;
      startX.value = event.clientX;
      startY.value = event.clientY;

      if (scale.value === 1) {
        // Zoom in
        const rect = imageRef.value?.getBoundingClientRect();
        if (!rect) return;

        const offsetX = event.clientX - rect.left;
        const offsetY = event.clientY - rect.top;

        scale.value = 2;  // Or any desired zoom level
        originX.value = (offsetX / rect.width) * 100;
        originY.value = (offsetY / rect.height) * 100;
      }
    };

    const stopDragging = () => {
      isDragging.value = false;
    };

    const onMouseMove = (event: MouseEvent) => {
      if (isDragging.value && scale.value > 1) {
        const dx = startX.value - event.clientX;
        const dy = startY.value - event.clientY;

        originX.value += (dx / imageRef.value!.width) * 100;
        originY.value += (dy / imageRef.value!.height) * 100;

        startX.value = event.clientX;
        startY.value = event.clientY;

        // Ensure origin values stay within bounds
        originX.value = Math.min(Math.max(originX.value, 0), 100);
        originY.value = Math.min(Math.max(originY.value, 0), 100);
      }
    };

    const resetZoom = () => {
      // Reset zoom
      scale.value = 1;
      originX.value = 50;
      originY.value = 50;
    };

    const imageStyles = computed(() => ({
      transform: `scale(${scale.value})`,
      transformOrigin: `${originX.value}% ${originY.value}%`,
      transition: isDragging.value ? 'none' : 'transform 0.1s ease'
    }));

    onMounted(updateImageSize);

    return {
      imageRef,
      containerRef,
      imageStyles,
      handleMouseDown,
      startDragging,
      stopDragging,
      onMouseMove,
      resetZoom,
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
  cursor: move;
  user-select: none; /* Prevents image selection */
}
</style>
