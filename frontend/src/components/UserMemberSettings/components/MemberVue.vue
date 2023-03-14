<template>
    <div @click="add" class="flex flex-col gap-3 items-center justify-center rounded-lg border-0 backdrop-blur-sm bg-white/40 w-full h-44 p-4" :class="[hover ? 'shadow-xl' : 'shadow-2xl']" @mouseover="hover = false" @mouseleave="hover = true">
        <div id="app-content" class="z-10 text-center" @click="showmodal">
            <div class="absolute select-none top-2 left-4">
                <p v-if="member.authorized" class="text-green-600 font-bold text-xl">Authorized</p>
                <p v-if="!member.authorized" class="text-red-800 font-bold text-xl">Deauthorized</p>
            </div>
            <div class="cursor-pointer" >
                <img :src="require(`@/assets/images/logo/zerotiericon.png`)" class="w-20" :class="{ grayscale : !member.authorized}">
            </div>
        </div>
        <div class="text-black text-base text-center font-semibold -mb-6 sm:mb-0 pointer-events-none select-none flex flex-col">
                <p>{{ member.address }} </p>
                <p>Time to live: {{member.timetolive == null ? "∞" : member.timetolive}}</p>
        </div>
        <p class="absolute bottom-1 left-3 pointer-events-none select-none"> {{ member.name }} </p>
    </div>


<i-modal v-model="visible">
    <template #header>
        Authorisierung
    </template>
        <div class="flex flex-col gap-4">
            <p>Bitte geben Sie den Grund an warum Sie das Gerät Authorisieren</p>
            <div class="flex flex-col gap-y-4">
                <i-form-group>
                    <i-form-label>Begründung</i-form-label>
                    <i-textarea v-model="reason" placeholder="Type something.." class="" />
                </i-form-group>
                <i-form-group>
                    <i-form-label>Zeitspanne</i-form-label>
                    <i-select v-model="duration" label="20:00 Uhr" placeholder="Choose something..">
                        <i-select-option value="20:00" label="20:00 Uhr"></i-select-option>
                        <i-select-option value="">None</i-select-option>
                        <i-select-option v-for="time in range(10,1)" :key="time" :value=time :label="`${time} Stunden`">{{ time }} Stunden</i-select-option>
                    </i-select>
                </i-form-group>
        </div>
        </div>
    <template #footer>
        <div class="flex gap-2 h-10 justify-center items-center">
            <p v-if="disabled" class="text-xl font-serif text-red-700">Bitte Einen Grund zun Authorisieren angeben</p>
            <i-button @click="authorize" v-if="!disabled" :disabled=disabled color="primary" block>Abschicken</i-button>
        </div>
    </template>
</i-modal>

</template>

<script setup>
import { ref, defineProps, defineEmits, computed } from 'vue'
const hover = ref(false)
const member = ref(props.member)
const visible = ref(false)
const disabled = computed(() => reason.value.length == 0)
const reason = ref("")
const duration = ref("20:00")
const props = defineProps(["member"])
const emit = defineEmits(['authorize', 'deauthorize'])

function showmodal(){
    if(member.value.authorized != true){
        visible.value = true
    }
    else{
        authorize()
    }
}

function range(size, startAt = 0) {
    return [...Array(size).keys()].map(i => i + startAt);
}

function authorize(){
    member.value.authorized = !member.value.authorized
    visible.value = false
    if(member.value.authorized){
        emit("authorize", member.value.address, reason, duration)
    }
    else{
        emit("deauthorize", member.value.address)
    }
    
}

</script>