<template>
  <p>Managed Routes {{routes.length + "/128"}}</p>
  <i-table color="dark" class="pt-2">
      <thead>
      <tr>
          <th>#</th>
          <th>Target</th>
          <th>via</th>
      </tr>
      </thead>
      <tbody v-for="route in routes" :key="route">
      <tr>
          <th scope="row"><button><i-icon @click="removeRouteReq" name="ink-times" class="text-red-900 mt-1" /></button></th>
          <td>{{route.target}}</td>
          <td>{{route.via ? route.via : "(LAN)"}}</td>
      </tr>
      </tbody>
  </i-table>
  <p>Add Routes</p>
  <div class="pt-2">
      <i-row >
          <i-column xs="4"><i-input v-model="destination" placeholder="Destination (CIDR)" /></i-column>
          <i-column xs="4"><i-input v-model="via" placeholder="Via (Optional)" /></i-column>
          <i-column class="self-center -ml-4"><button><i-icon name="ink-plus" @click="addRouteReq" class="_color:success" /></button></i-column>
      </i-row>
  </div>
</template>
    
<script setup>
import { defineProps, ref, defineEmits } from 'vue';
/* eslint-disable */
import { validateIP, normilizeIP, validateCIDR } from "@/components/utils/IP";

const routes = ref(props.routes)
const destination = ref()
const via = ref()
    
const props = defineProps({
    routes : Object,
})

const emit = defineEmits(['change'])

function removeRouteReq(index){
    routes.value.splice(index, 1);
    emit("change", routes.value);
  };

function addRouteReq(){
    let data = {};
    if (validateCIDR(destination.value)) {
      data["target"] = destination.value;
    } else {
      return;
    }
    if (via.value && validateIP(via.value)) {
      data["via"] = normilizeIP(via.value);
    }


    routes.value.push(data);
    emit("change", data);
    
    destination.value = "";
    via.value = "";
  };
    
 
</script>