<template>
  <router-view />
</template>
<script >
import { defineComponent } from "vue";

export default defineComponent({
  setup() {
    const debounce = (callback, delay) => {
      let tid;
      return function (...args) {
        const ctx = this; // 在 JS 中通常用 `this` 而不是 `self` 来引用当前的上下文
        if (tid) clearTimeout(tid);
        tid = setTimeout(() => {
          callback.apply(ctx, args);
        }, delay);
      };
    };

    const OriginalResizeObserver = window.ResizeObserver;
    window.ResizeObserver = class ResizeObserver extends OriginalResizeObserver {
      constructor(callback) {
        super(debounce(callback, 20));
      }
    };
  },
});

</script>


<style>
#app {
  font-family: Arial, Helvetica, sans-serif;
  height: 100%;
}
</style>