<template>
    <div class="rounded-lg">
        <p class="font-semibold text-lg text-emerald-600">{{ props.tagname }}</p>
        <div class="grid grid-cols-2">

            <i-button @click="onValueChange" block>{{ foundenum }}</i-button>
            <div class="flex">
                <i-number-input v-model="foundtag" disabled placeholder="Type something.." @click="onValueChange"></i-number-input>
                <button><i-icon name="ink-times" class="_color:danger" @click="onValueChange" /></button>
            </div>
        </div>
        

    </div>
    
</template>
        
<script setup>
import { defineProps, ref, defineEmits, onMounted } from 'vue';
/* eslint-disable */
// eslint-disable-next-line
const member = ref(props.member)
const tag = ref(props.tag)
const tagnum = ref()
const visible = ref(true)
const enums = ref()
const foundtag = ref("")
const foundenum = ref("")

const props = defineProps({
    member : Object,
    tag    : Object,
    tagname : String
})
// eslint-disable-next-line  
const emit = defineEmits(['change'])

onMounted(findTag)

function onValueChange () {
    for (const tag in member.value.config.tags){
        if (props.tag.id == member.value.config.tags[tag][0]){
            member.value.config.tags.splice(tag, 1)
        }
    }
    
    emit("change")
}

function getKeyByValue (object, value) {
  return Object.keys(object).find(key => object[key] == value);
}

function findTag () {
    for (const index in member.value.config.tags){
        if (props.tag.id == member.value.config.tags[index][0]){
            foundtag.value = member.value.config.tags[index][1]
            foundenum.value = getKeyByValue(tag.value.enums, foundtag.value)
            break
        }
        else {
            foundtag.value = "Fehler"
        }
    }
}
 
</script>