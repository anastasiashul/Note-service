const fs = require('fs');
const path = require('path');
function test_on_structure() {
    try {

        const requiredFiles = [
            'index.html',
            'style.css',
            'app.js'
        ];
        let allPassed = true;

        requiredFiles.forEach(file => {
            const filePath = path.join(__dirname, '..', file);
            if (fs.existsSync(filePath)) {
                console.log(`${file} exists`);
            } else {
                console.log(`${file} not found`);
                allPassed = false;

            }
        });

        console.log('Frontend structure check completed!');
        return allPassed;

    } catch (error) {
        console.error('Test failed:', error.message);
        return false;
    }
}
module.exports = { test_on_structure};
