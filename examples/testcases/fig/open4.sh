#!/bin/sh
echo Quick, change desktop
sleep 1
xpdf -remote one -geometry 400x580+0+2 -z 90 1/test.pdf&
xpdf -remote two -geometry 400x580+400+2 -z 90 2/test.pdf&
xpdf -remote three -geometry 400x580+800+2 -z 90 3/test.pdf&
xpdf -remote four -geometry 400x580+1200+2 -z 90 4/test.pdf&
xpdf -remote five -geometry 400x580+0+582 -z 90 5/test.pdf&
xpdf -remote six -geometry 400x580+400+582 -z 90 5/test.pdf&
xpdf -remote seven -geometry 400x580+800+582 -z 90 5/test.pdf&
xpdf -remote eight -geometry 400x580+1200+582 -z 90 5/test.pdf&
sleep 1
xpdf -remote one -exec toggleOutline 
sleep 0.2
xpdf -remote two -exec toggleOutline
sleep 0.2
xpdf -remote three -exec toggleOutline
sleep 0.2
xpdf -remote four -exec toggleOutline
xpdf -remote five -exec toggleOutline
xpdf -remote six -exec toggleOutline
xpdf -remote seven -exec toggleOutline
xpdf -remote eight -exec toggleOutline
