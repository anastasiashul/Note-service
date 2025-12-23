console.log('Starting frontend tests...');
const basicTests = require('./basic-tests.js');

const structureResult =basicTests.test_on_structure();

if (structureResult) {
    console.log('\n All frontend tests completed!');
    process.exit(0);
}
else {
    console.log('Some tests failed');
    process.exit(1);
}
