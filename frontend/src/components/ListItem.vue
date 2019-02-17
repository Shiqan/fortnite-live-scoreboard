<template>
    <div>
        <h1>{{ item.eliminator }}</h1>
        <h2>{{ item.kills }} -- {{ item.knocks }}</h2>
        <span>{{ status() }}</span>
    </div>
</template>

<script>
export default {
    name: "ListItem",
    props: ['item'],
    methods: {
        status: function() {
            if (this.item.died) {
                return "Died";
            }
            if (this.item.knocked) {
                return "Knocked";
            }
            return "Alive";
        }
    }
};
</script>
