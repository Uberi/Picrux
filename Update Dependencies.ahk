#NoEnv

Path := A_ScriptDir

try {
    UrlDownloadToFile, http://code.jquery.com/jquery.min.js, %Path%\views\lib\jquery.min.js
    UrlDownloadToFile, http://code.jquery.com/jquery.min.map, %Path%\views\lib\jquery.min.map
}
catch e
    MsgBox, Error updating jQuery.

try
    UrlDownloadToFile, http://momentjs.com/downloads/moment-with-langs.min.js, %Path%\views\lib\moment-with-langs.min.js
catch e
    MsgBox, Error updating MomentJS.

try
    UrlDownloadToFile, https://raw.github.com/wanasit/chrono/master/chrono.min.js, %Path%\views\lib\chrono.min.js
catch e
    MsgBox, Error updating ChronoJS.

try
    UrlDownloadToFile, https://raw.github.com/chjj/marked/master/lib/marked.js, %Path%\views\lib\marked.js
catch e
    MsgBox, Error updating Marked.