<template>
    <div>
        <v-expansion-panel v-if="r" expand style="box-shadow: none">
            <v-expansion-panel-content v-for="(event, i) in p" :key="i" hide-actions>
                <v-layout slot="header" row style="align-items: center">
                    <v-flex xs8><span style="font-weight: bold;">{{event.title}}</span></v-flex>
                    <v-flex xs1></v-flex>
                    <v-flex xs3><a class="date">{{event.date}}</a></v-flex>
                </v-layout>
                <v-card>
                    <v-layout wrap>
                        <v-flex xs12>{{event.about}}</v-flex>
                        <br>
                        <div style="justify-content: center">
                            <v-btn class="go" color="#2196F3" dark @click="vote(0, event.id)">Пойду({{event.yes}})</v-btn>
                            <v-btn class="notgo" color="#FF5252" dark @click="vote(1, event.id)">Не пойду({{event.no}})</v-btn>
                        </div>
                    </v-layout>
                </v-card>
            </v-expansion-panel-content>
        </v-expansion-panel>
    </div>
</template>

<script>
    export default {
        name: "poll",
        props: ['p', 'r'],
        methods:{
            vote(mode, id){
                if (mode == 0){
                    this.$emit('vote', ["yes", id]);
                }
                else {
                    this.$emit('vote', ["no", id]);
                }
            }
        }
    }
</script>

<style scoped>
    .date {
        color: white;
        background-color: #ffb533;
        border-radius: 7px;
        padding: 3px;
        clear: right;
    }

    li {
        border-radius: 4px;
    }

    ul {
        border-radius: 4px;
    }

    .v-card {
        border-radius: 10px !important;
    }

    .v-window {
        border-radius: 10px !important;
    }

    .v-expansion-panel__body .v-card {
        border-radius: 1em
    }

    .v-expansion-panel__body,
    .v-expansion-panel__body .v-card .v-card__text,
    .v-card {
        border-radius: 1em;
        width: 90%;
        margin-left: 5%;
    }

    .v-expansion-panel__container--active,
    .v-expansion-panel__container--active {
        margin: 0;
    }

    .v-expansion-panel__container {
        box-shadow: none;
        padding-bottom: 3px;
        border-radius: 1em;
    }

    @media screen and (min-width: 600px) {
        .v-expansion-panel__container:hover {
            box-shadow: none;
            cursor: pointer;
        }
    }

    .go {
        font-size: medium;
    }

    .notgo {
        font-size: medium;
    }
</style>
