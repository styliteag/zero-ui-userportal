<template>
    <div class="pt-2">
        <button><i-icon name="ink-times" class="_color:danger" @click="visible = true" /></button>
    </div>
 
<i-modal v-model="visible" color="warning" transition="fade-in-transition">
    <template #header>
        <p>Are you sure you want to delete this member?</p>
    </template>
    <p>This action cannot be undone.</p>
    <div class="flex gap-x-8 pt-14 justify-center">
        <i-button color="danger" @click="DeleteMember" >
            Delete
        </i-button>
        <i-button color="dark" @click="visible = false">
            Cancel
        </i-button>
    </div>

</i-modal>
</template>
        
<script setup>
import { defineProps, ref, defineEmits } from 'vue';

const visible = ref(false)

/* eslint-disable */
const props = defineProps({
    member : Object,
})
    
const emit = defineEmits(['deletemember'])

function DeleteMember(){
    visible.value = false;
    emit('deletemember');

}
    

        
 
</script>