<template>
    <i-collapsible-item name="Flow Rules" title="Flow Rules" class="z-[988] ">
        <div class="flex gap-x-2">
            <div class="w-3/4">
                <Codemirror class="rounded-xl" v-model:value="network.rulesSource" :options="cmOptions" @change="flows" @ready="flows" />
            </div>
            <i-button class="self-center" color="warning" size="lg" @click="emit('sendrequest')">Save Changes</i-button>
            <div class="w-1/4">
                <CodeEditor width="auto" height="850px" font_size="11px" :value=flowRules :language_selector="false" :hide_header="true" :read_only="true" :copy_code="true" :languages="[['json', 'json']]"></CodeEditor>
            </div>
        </div>
    </i-collapsible-item>

</template>
<script setup>
import { ref, defineEmits, defineProps, computed, onMounted } from "vue";
import CodeEditor from 'simple-code-editor';

import { compile } from "./components/RuleCompiler.js";

import Codemirror from "codemirror-editor-vue3";
// language
import "codemirror/mode/javascript/javascript.js";
// theme
import "codemirror/theme/ayu-mirage.css";


/* eslint-disable */
const network = ref(props.network)

const cmOptions = {
        mode: "text/javascript", // Language mode
        theme: "ayu-mirage", // Theme
        lineNumbers: true, // Show line number
        smartIndent: true, // Smart indent
        indentUnit: 2, // The smart indent unit is 2 spaces in length
        styleActiveLine: true, // Display the style of the selected row
        foldGutter: true
      }
const flowdata = ref({
    rules: [...network.value.config.rules],
    capabilities: [...network.value.config.capabilities],
    tags: [...network.value.config.tags],
  })
const flowRules = computed(() => JSON.stringify(flowdata.value, null, 2))

const emit = defineEmits(["sendrequest"])

const props = defineProps({
    network : Object,
})

onMounted(flows)


function flows(){
    let rules = [],
      caps = {},
      tags = {};
    const res = compile(network.value.rulesSource, rules, caps, tags);
    if (!res) {
      let capabilitiesByName = {};
      for (var key in caps) {
        capabilitiesByName[key] = caps[key].id;
      }

      let tagsByName = { ...tags };
      for (let key in tags) {
        tags[key] = { id: tags[key].id, default: tags[key].default }
      }

      flowdata.value = {
        rules: [...rules],
        capabilities: [...Object.values(caps)],
        tags: [...Object.values(tags)],
      }

      network.value.tagsByName = tagsByName
      network.value.capabilitiesByName = capabilitiesByName
    }
}


</script>