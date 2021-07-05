let camera, scene, renderer, controls;

const config = {

    background: 0x000000,
    highlight_color: new THREE.Color(0xffffff),
    camera_x: 5,
    camera_y: 5,
    camera_z: 10

};
    
init = function() {

    scene = new THREE.Scene()

    const width = document.getElementById('display').clientWidth;
    const height = document.getElementById('display').clientHeight;

    camera = new THREE.PerspectiveCamera(50, width/height, 0.1, 1000);

    camera.position.x = config.camera_x;
    camera.position.y = config.camera_y;
    camera.position.z = config.camera_z;

    renderer = new THREE.WebGLRenderer({antialias:true, alpha:true});
    renderer.setPixelRatio(window.devicePixelRatio ? window.devicePixelRatio : 1);
    renderer.setClearColor(config.background, 1);
    renderer.setSize(width, height);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.zoomSpeed = 0.5;

    document.getElementById('display').appendChild(renderer.domElement);
    
};

render = function() {

    requestAnimationFrame(render);
    renderer.render(scene, camera);

};

load = function(gltf_file_name) {

    const asset = gltf_file_name;
    const gltf_loader = new THREE.GLTFLoader();
    
    gltf_loader.load(

	asset,

	function(gltf) {
	    
	    scene.add(gltf.scene);	    
	},

	function(xhr) {

	    let percentComplete = Math.round((xhr.loaded / xhr.total)*100);
	    console.log(percentComplete+'% loaded');
	    
	},

	function(error) {

	    console.log("An error occured loading the glb file");

	}

    );
    
};
