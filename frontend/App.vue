<template>
    <v-app id="app">
        <v-toolbar style="align-items: center; z-index: 1" flat color="transparent"
                   dark height="55em">
            <v-flex xs1>
                <v-card flat id="logo" transparent color="transparent" :to="'/'">
                    <img src="../static/DG.png" height="52em" style="margin-top: 4px" alt="">
                </v-card>
            </v-flex>
            <!--a class="white--text" style="font-size: 3.5em; margin: 1% 0 0 -1.5%; opacity: 0" id="wallet">Wallet</a-->
            <v-spacer></v-spacer>
            <div class="text-xs-center">
            </div>
        </v-toolbar>
        <v-layout justify-space-between align-center
                  style="background-color: black; width: 100%; margin: 0; align-items: center; margin-top: -55px"
                  height="50vh">
            <div style="text-align: center; display: block; margin-left: auto; margin-right: auto;">
                <img src="../static/polytech_logo.svg" width="400vw" height="400vw"/>
            </div>
        </v-layout>
        <v-layout id="layout" style="height: 65vh">
            <v-flex xs1></v-flex>
            <div id="rectangle"></div>
            <v-flex xs10>
                <v-item-group
                        v-model="currentWindow"
                        class="text-xs-center"
                        mandatory>
                    <v-item>
                        <v-btn
                                slot-scope="{ active, toggle }"
                                :input-value="active"
                                icon
                                @click="toggle"
                                :to="'/'">
                            <v-icon style="filter: invert(100%);">calendar_today</v-icon>
                        </v-btn>
                    </v-item>
                    <!--<v-item>-->
                    <!--<v-btn-->
                    <!--slot-scope="{ active, toggle }"-->
                    <!--:input-value="active"-->
                    <!--icon-->
                    <!--@click="toggle"-->
                    <!--:to="'/announces'">-->
                    <!--<v-icon style="filter: invert(100%);">poll</v-icon>-->
                    <!--</v-btn>-->
                    <!--</v-item>-->
                </v-item-group>
                <v-card
                        flat
                        tile>
                    <v-window v-model="currentWindow" style="z-index: 9" mandatory>
                        <v-window-item>
                            <v-card>
                                <announces :p="events" :r="eventsready" @vote="Vote"></announces>
                            </v-card>
                        </v-window-item>
                        <!--<v-window-item>-->
                        <!--<v-card>-->
                        <!--<router-view></router-view>-->
                        <!--</v-card>-->
                        <!--</v-window-item>-->
                    </v-window>
                </v-card>
            </v-flex>
            <v-flex xs1></v-flex>
        </v-layout>
        <v-snackbar v-model="isvote" :timeout="7000" bottom color="#4CAF50">
            Ваш голос принят!
        </v-snackbar>
    </v-app>
</template>

<script>
    import announces from './components/announce'
    import axios from 'axios'

    export default {
        name: 'App',
        components: {announces},
        data() {
            return {
                //
                isAnnounces: true,
                currentWindow: 0,
                length: 2,
                id: "19",
                result: "yes",
                events: [],
                isvote: false,
                eventsready: false
            }
        },
        methods: {
            checkResponse(r) {
                if ((r.status == 200 || r.status == 201 || r.status == 202 || r.status == 203 || r.status == 204 || r.status == 205 || r.status == 206) || r.data.message == "OK") {
                    console.log("response – ok");
                    return true; //if ok
                } else {
                    console.log("!! error", r);
                    return false;
                }
            },
            Vote(i) {
                const pre_vote = {
                    "id": i[1].toString(),
                    "result": i[0],
                };
                const votejson = JSON.stringify(pre_vote);
                console.log(votejson);
                axios.post("https://politex.herokuapp.com/" + 'vote', votejson).then(response => {
                    if (this.checkResponse(response)) {
                        this.isvote = true;
                        return true;
                    }
                });
            },
            GetEvents() {
                axios.get("https://politex.herokuapp.com/" + 'events').then(response => {
                        if (this.checkResponse(response)) {
                            this.events = response.data;
                            // for (let j = 0; j < (abc.length); j++) {
                            //     console.log(abc[j].id === (j ).toString());
                            //         if (abc[j].id === (j + 1).toString()) {
                            //             console.log('HERE');
                            //             let def = {};
                            //             def.id = abc[j].id;
                            //             def.about = abc[j].about;
                            //             def.date = abc[j].date;
                            //             def.picture = abc[j].picture;
                            //             def.title = abc[j].title;
                            //             def.yes = abc[j].yes;
                            //             def.no = abc[j].no;
                            //             this.events[j] = def;
                            //         }
                            //
                            // }
                            this.eventsready = true;
                            console.log(this.events);
                            return true;
                        }
                    }
                )
            }
        },
        mounted() {
            this.GetEvents()
            //this.Vote()
        }
    }
</script>
<style>
    #layout {
        background: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 11, 70, 1) 100%);
    }

    #rectangle {
        top: 550px;
        left: -500px;
        width: 200vw;
        height: 50vw;
        transform: rotate(15deg);
        background-color: #94e652;
        z-index: 0;
        position: absolute;
    }

    #app {
        font-family: 'Google Sans'
    }
</style>
