# Distribution

## macOS App (Intel chip only)

Important NOTE: When an application gets downloaded from any source other than those that Apple seems suited, the application gets an extended attribute "com.apple.Quarantine".
This triggers the message: "application XY is damaged and can't be opened. You should move it to the Bin."

Remove the attribute and you can launch the application.

So after download: open a console and type:
```
$ xattr -c <path/to/application.app>
```
After that you can run the App as usual.

- 2026-05may-28, Version 3.0.30, https://www.flagsoft.com/public/ptxprint/2026-05may-28/PTXprint.zip
