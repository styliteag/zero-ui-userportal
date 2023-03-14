<template>
    <div class="pt-2">
        <div v-if="member.config.ipAssignments.length <= 1">
            <div v-for="ipAssignment, index  in member.config.ipAssignments" :key="index" class="flex">
                <p>{{ ipAssignment }}</p>
                <button><i-icon name="ink-times" class="_color:danger" @click="removeipAssignments(index)" /></button>
            </div>
        </div>
        <div v-else>
            <button @click="visible = true">{{member.config.ipAssignments.length}} IP Assignments</button>
        </div>
        <i-row class="pt-2.5">
            <i-column class="flex">
                <i-input v-model="ipInput" />
                <button><i-icon name="ink-plus" class="self-center _color:success"  @click="addipAssignmentsindex"/></button>
            </i-column>

        </i-row>
    </div>

<i-modal v-model="visible">
    <template #header>
        Modal Header
    </template>
    <div v-for="ipAssignment, index  in member.config.ipAssignments" :key="index" class="flex">
        <p>{{ ipAssignment }}</p>
        <button><i-icon name="ink-times" class="_color:danger" @click="removeipAssignments(index)" /></button>
    </div>
</i-modal>
</template>
        
<script setup>
import { defineProps, ref, defineEmits } from 'vue';



const member = ref(props.member)
const ipInput = ref("")
const visible = ref(false)


const props = defineProps({
    member : Object,
})
    
const emit = defineEmits(['change'])

function removeipAssignments(index){
    member.value.config.ipAssignments.splice(index, 1);
    emit("change", member.value.config.ipAssignments);
}
    
function addipAssignmentsindex(){
    member.value.config.ipAssignments.push(ipInput.value);
    ipInput.value = ""
    emit("change", member.value.config.ipAssignments);
}
    

        
 
</script>