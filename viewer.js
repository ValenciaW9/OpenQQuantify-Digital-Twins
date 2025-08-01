/*Valencia Walker's viewer.js*/
Cesium.Ion.defaultAccessToken = 'YOUR_CESIUM_ION_ACCESS_TOKEN';

const viewer = new Cesium.Viewer('cesiumContainer', {
    terrainProvider: Cesium.createWorldTerrain()
});

viewer.scene.globe.enableLighting = true;


Cesium.Ion.defaultAccessToken = 'your_actual_token_here';

const assetId = YOUR_ASSET_ID; // Replace with actual ID from Cesium Ion
viewer.scene.primitives.add(Cesium.Cesium3DTileset.fromIonAssetId(assetId));

