<template>
    <i-collapsible-item name="Network Management" title="Network Management">
        <div class="flex gap-x-2">
          <i-button color="danger" @click="emit('sendrequest')">DELETE NETWORK</i-button>
        </div>
    </i-collapsible-item>

</template>
<script setup>
import { ref, defineEmits, defineProps} from "vue";

/* eslint-disable */
const network = ref(props.network)
const emit = defineEmits(["sendrequest"])

const props = defineProps({
    network : Object,
})



</script>