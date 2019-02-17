<template>
    <div class="hello">
        <h1>{{ msg }}</h1>
        <list-item v-bind:item="item" v-for="item in orderedStandings" :key="item.eliminator"></list-item>
    </div>
</template>

<script>
import ListItem from "@/components/ListItem";

export default {
    name: "HelloWorld",
    components: {
      ListItem
    },
    data() {
        return {
            standings: [],
            msg: "Welcome to Your Vue.js App"
        };
    },
    mounted() {
        this.$socket.emit("message", "hello!");
    },
    computed: {
        orderedStandings: function() {
            return this.standings.slice(0).sort((a, b) => {
                if (a.kills < b.kills) {
                    return 1;
                }
                if (a.kills > b.kills) {
                    return -1;
                }
                return 0;
            });
        }
    },
    methods: {
        doesExists(player) {
            for (let i = 0; i < this.standings.length; i++) {
                if (this.standings[i].eliminator === player) {
                    return i;
                }
            }
            return -1;
        }
    },
    sockets: {
        connect() {
            console.log("connected to ws server");
        },
        message(data) {
            let eliminator = data.msg.Eliminator;
            let eliminated = data.msg.Eliminated;
            let died = !data.msg.Knocked;

            var i = this.doesExists(eliminator);
            if (i >= 0) {
                if (died) {
                    this.standings[i].kills += 1;
                    this.standings[i].knocks -= 1;
                } else {
                    this.standings[i].knocks += 1;
                }
            } else {
                this.standings.push({
                    eliminator: eliminator,
                    kills: (died) ? 1 : 0,
                    knocks: (!died) ? 1 : 0,
                    knocked: false,
                    died: false
                });
            }

            i = this.doesExists(eliminated);
            if (i >= 0) {
                if (died) {
                    this.standings[i].died = died;
                } else {
                    this.standings[i].knocked = true;
                }
            } else {
                this.standings.push({
                    eliminator: eliminated,
                    kills: 0,
                    knocks: 0,
                    knocked: !died,
                    died: died
                });
            }
        }
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
    font-weight: normal;
}
ul {
    list-style-type: none;
    padding: 0;
}
li {
    display: inline-block;
    margin: 0 10px;
}
a {
    color: #42b983;
}
</style>
