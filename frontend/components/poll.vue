<template>
    <div>
        <v-expansion-panel v-if="p" expand style="box-shadow: none">
            <v-expansion-panel-content v-for="(event, i) in p" :key="i" hide-actions>
                <v-layout slot="header" row style="align-items: center">
                    <h1>{{event.title}}</h1>
                </v-layout>
            </v-expansion-panel-content>
        </v-expansion-panel>
    </div>
</template>

<script>
    export default {
        name: "sec",
        props: ['p'],
        data: () => ({

        }),
        mounted() {
        },
        methods:{

        }
    }
</script>

<style scoped>

</style>
