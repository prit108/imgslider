/* Image Division
 ** Authors: prit108, cipherLord, jaingaurav1601
 */

var ImagePuzzle_ImageActions = {

    loadImage: function(gameCnt, imgsrc, callback) {

        var img = new Image();

        img.onerror = function() {

            $('<div><p>Please choose a stock image\nor paste a valid url</p></div>').dialog({
                modal: true,
                title: 'Invalid image',
                buttons: [{
                    text: "Ok",
                    click: function() {
                        $(this).dialog("close");
                    }
                }]
            });
        };

        img.onload = function() {

            callback(img);
        };

        if (gameCnt == 1) {
            document.getElementById("refImgSrc").src = "/static/images/preview/numbers.png"
        } else {
            document.getElementById("refImgSrc").src = imgsrc;
        }
        img.src = imgsrc;

    },

    /*
     * Function Split 
     * Description: splits an image into a number or canvas elements
     * 
     * Paramaters: Path to image and the number of tiles required
     *             Ex 9 tiles for a 3x3 image. tiles must be a 
     *             number squared
     * Returns: an Array of canvasElements (Images)            
     *
     */
    split: function(canvas, tiles, gameCnt) {

        var canvasArray = new Array();

        var row_col = Math.sqrt(tiles),
            tileH = Math.round(canvas.height / row_col),
            tileW = Math.round(canvas.width / row_col),
            xoffset = 0,
            yoffset = 0,
            imgNumBgSizeWidth,
            imgNumXOffset;

        for (var i = 0; i < tiles; i++) {

            //create canvas element and set attributes and get the canvas context
            canvasArray[i] = document.createElement('canvas');
            canvasArray[i].setAttribute('width', tileW);
            canvasArray[i].setAttribute('height', tileH);
            canvasArray[i].setAttribute('id', 'canvas' + i);
            var ctx = canvasArray[i].getContext('2d');

            ctx.drawImage(canvas, xoffset, yoffset);

            if (i + 1 > 9) {

                imgNumBgSizeWidth = 16;
                imgNumXOffset = 1;

            } else {

                imgNumBgSizeWidth = 10;
                imgNumXOffset = 2;
            }
            var height = 10
            var size = 10
            if (gameCnt == 1) {
                height = tileH
                imgNumBgSizeWidth = tileW
                size = 100
                ctx.fillStyle = 'rgba(255, 255, 255, 1)';
                ctx.fillRect(0, 0, tileW, tileH);
                ctx.fillStyle = '#000';
                ctx.font = 'italic 100px sans-serif';
                ctx.textBaseline = 'top';
                ctx.fillText(i + 1, tileW / 2 - 50, tileH / 2 - 50);
            } else if (gameCnt == 5) {
                var numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34];
                height = tileH
                imgNumBgSizeWidth = tileW
                size = 100
                ctx.fillStyle = 'rgba(255, 255, 255, 1)';
                ctx.fillRect(0, 0, tileW, tileH);
                ctx.fillStyle = '#000';
                ctx.font = 'italic 100px sans-serif';
                ctx.textBaseline = 'top';
                ctx.fillText(numbers[i], tileW / 2 - 75, tileH / 2 - 75);
            }
            //draw tile numbers


            //if i is a multiple of the total number of tiles to a row,
            //move down a column and reset the row_col
            if ((i + 1) % row_col == 0) {
                yoffset -= tileH;
                xoffset = 0;
            } else {
                //otherwise move across the image
                xoffset -= tileW;
            }
        }

        return canvasArray;
    },

    /*
     *  Function ResizeImage
     *  Description: Resizes an image to half the screen height and half the 
     *         screen width.
     *  Parameters: The Image path
     *  Returns: A resized canvas Element (Image)
     *
     */
    resize: function(loadedImage, callback) {

        var img = new Image(),
            canvas = document.createElement('canvas'),
            ctx = canvas.getContext("2d");

        img.onload = function() {

            //maximum image size
            canvas.width = screen.width / 2 + 100;
            canvas.height = screen.height / 2 + 100;
            ctx.drawImage(img, 0, 0, screen.width / 2 + 100, screen.height / 2 + 100);

            callback(canvas);
        };

        img.src = loadedImage.src;
    }
};