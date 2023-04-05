const axios = require('axios').default;
const BEARER_TOKEN = 'Bearer be4d3d0279e64ff88cfe9a18c2d38c39';

exports.handleImageUpload = async (event, context) => {
    const file = event;
    const filePath = file.name;
    const targetFilePath = buildTargetFilePath(filePath);
    console.log("starting process for file", filePath);

    const isNotImage = !isImage(file)
    const isNotInBaseFolder = !filePath.startsWith('fotos-originais/')
    const isInOldPicFolder = filePath.includes('fotos-antigas')
    if (isNotImage || isNotInBaseFolder || isInOldPicFolder) return;
   
    // claid.ai resize request
    await makeRequest({
        "input": "storage://property/" + filePath,
        "operations": {
            "restorations": {
                "upscale": "photo"
            },
            "resizing": {
                "width": 1440,
                "height": 960,
                "fit": {
                    "crop": "smart"
                }
            },
            "adjustments": {
                "hdr": 100
            }
        },
        "output": {
            "destination": "storage://property/" + targetFilePath,
            "format": {
                "type": "jpeg",
                "quality": 75,
                "progressive": true
            }
        }
    })
};

function buildTargetFilePath(source) {
    const baseFolderChanged = source.replace("fotos-originais/", "fotos-otimizadas/");
    return baseFolderChanged.replace(/\.[^.]+$/, ".jpg");
}

function isImage(file) {
    const allowedMimeTypes = ['image/jpeg', 'image/png', 'image/gif'];
    return allowedMimeTypes.includes(file.contentType)
}

async function makeRequest(payload) {
    const endpoint = "https://api.claid.ai/v1-beta1/image/edit";
    const config = { headers: { 'Authorization': BEARER_TOKEN } };

    try {
        await axios.post(endpoint, payload, config);
        console.log(`file saved successfully`)
    } catch (error) {
        console.error(error)
    }
}