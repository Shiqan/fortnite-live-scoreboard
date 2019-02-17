const server = require("server");
const { get, socket } = require("server/router");
const mqtt = require("mqtt");

// get server port from environment or default to 3000
const port = process.env.PORT || 3000;
var subscribed = false;
const mqttclient = mqtt.connect("mqtts://m24.cloudmqtt.com", {
    clientId: "mqttjs_" + Math.random().toString(16),
    username: "Node",
    password: "H6!JLzje6!8gdSf8FdxJ5@d8!djb8fzp",
    port: "28142"
});

mqttclient.on("connect", () => {
    console.log("connected");
    mqttclient.subscribe("Fortnite/#");
});

mqttclient.on("error", error => {
    console.error("Can't connect" + error);
});

server({ port }, [
    get("/", ctx => "<h1>Hello you!</h1>"),
    socket("connect", ctx => {
        console.log("client connected", Object.keys(ctx.io.sockets.sockets));

        if (!subscribed) {
            mqttclient.on("message", (topic, message) => {
                console.log("received message %s %s", topic, message);
                ctx.io.emit("message", {
                    msg: JSON.parse(message.toString())
                });
            });
            subscribed = true;
        }    
    })
]).then(() => {
    console.log(`Server running at http://localhost:${port}`);
    return 200;
});
