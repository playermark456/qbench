// Prod template

importScripts('https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js');
importScripts('https://d731z7k534aiw.cloudfront.net/v2.7.0/qbjs.js');

// Documentation for QBJS: https://qbjs.docs.qbench.net

run(() => {

    const qbConsole = QB.console;         // Object to write to the console
    const qbProgressBar = QB.progressBar; // Object to control the progress bar
    const files = QB.files;               // Array of files selected to upload 

    try {
        // Your code here...

        /* ---------------------------------- */
        /* Example Code */
        qbProgressBar.setPercentage(0);
        qbConsole.clear();
        
        qbConsole.log('Begin process...');
        qbConsole.log(`Files to process: ${files.length}`);
        qbProgressBar.setPercentage(50);
        setTimeout(() => {
            qbProgressBar.setPercentage(100);
            qbConsole.log('Finished!');

            // Notifies QBench that the script finished successfully
            // NOTE: should be included in every file parser script
            QB.success();
        }, 3000);
        /* ---------------------------------- */ 
    } catch(e) {
        // Notifies QBench that the script finished with an error
        // NOTE: should be included in every file parser script
        qbConsole.log(`ERROR: ${e.message}`);
        QB.error();
    }
});
