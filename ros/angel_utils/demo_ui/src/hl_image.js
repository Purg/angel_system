// Create a listener for compressed images with bounding boxes
var image_listener = new ROSLIB.Topic({
    ros : ros,
    name : workspace + '/pv_image_detections_2d/compressed',
    messageType : 'sensor_msgs/msg/CompressedImage' // find: $ ros2 topic type <>
});

image_listener.subscribe(function(m) {
    // update image
    var image = document.getElementById('hl-image');
    image.src = "data:image/jpeg;base64," + m.data;
});