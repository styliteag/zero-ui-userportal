<template>
    <div class="rounded-lg">
        <p class="text-lg text-red-600">{{ props.tagname }}</p>
        <div class="grid grid-cols-2">
            <div>
                <i-select v-if="visible" :placeholder=enums @search="setEnum">
                    <div v-for="enu in Object.keys(tag.enums)" :key="enu">
                        <i-select-option :value=enu :label=enu />
                    </div>
                </i-select>
                <i-button v-else @click="(visible = true)" block>{{ enums }}</i-button>
            </div>
            <i-number-input v-model="tagnum" placeholder="..." @change="setEnumSelect"></i-number-input>    
        </div>


    </div>
    
</template>
        
<script setup>
import { defineProps, ref, defineEmits } from 'vue';
/* eslint-disable */
// eslint-disable-next-line
const member = ref(props.member)
const network = ref(props.network)
const tag = ref(props.tag)
const tagnum = ref()
const visible = ref(true)
const enums = ref()

const props = defineProps({
    member : Object,
    network: Object,
    tag    : Object,
    tagname : String
})
// eslint-disable-next-line  
const emit = defineEmits(['change'])

function getKeyByValue (object, value) {
  return Object.keys(object).find(key => object[key] == value);
}

function setEnum (enu) {
    tagnum.value = tag.value.enums[enu]
    onValueChange()
}

function setEnumSelect () {
    const key = getKeyByValue(tag.value.enums, tagnum.value)
    if (key != undefined){
        visible.value = false
        enums.value = key
        onValueChange()
    }
}

function onValueChange () {
    for (const index in member.value.config.tags){
        if (props.tag.id == member.value.config.tags[index][0]){
        member.value.config.tags.splice(index, 1)
        }
    }
    member.value.config.tags.push([props.tag.id, parseInt(tagnum.value)])
    emit("change")
}
 
</script>