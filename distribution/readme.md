# Distribution

This is an non-official distribution of PTXprint for macOS with Intel(TM) chips.

<img width="640"  alt="02-layout" src="https://github.com/user-attachments/assets/a1917c06-a062-4775-b1d8-f84b1e6ac294" />



## Download macOS App (for Intel chip only)

Download any version here:
https://www.flagsoft.com/public/ptxprint/

ba288c6d028d500020876174ccd57921f94789ced71882a11af1cd2628dda60b, 3.0.32, PTXprint.zip


<!--
### 2026-06jun-01, Version 3.0.31, https://www.flagsoft.com/public/ptxprint/2026-06jun-01/PTXprint.zip

sha256sum of ZIP file: ad1b6436f35650e404fc072e72f5ec3b663e78b2de8dc8fcc62aed3a5eb8e377
-->

<!--
### 2026-05may-28, Version 3.0.30, https://www.flagsoft.com/public/ptxprint/2026-05may-28/PTXprint.zip

sha256sum of ZIP file: 19f6129608b88e5a1343d93c94d4480c10a37863592cc7e578c450deeba4bda4
-->



### Important NOTE after downloading .app file

When an application gets downloaded from any source other than those that Apple seems suited, the application gets an extended attribute "com.apple.Quarantine".
This triggers the message: "application XY is damaged and can't be opened. You should move it to the Bin."

Remove the attribute and you can launch the application.

So after download: open a console and type:
```
$ xattr -c <path/to/application.app>
```
After that you can run the App as usual.



### You must Install XeTeX separately

You *must* install XeTeX with brew (Homebrew), see https://brew.sh/ else it will not work.

```
% brew install xetex
```

This will install XeTeX with binaries:

```
/usr/local/bin/fc-list
/Library/TeX/texbin/xetex
/Library/TeX/texbin/xdvipdfmx
```



