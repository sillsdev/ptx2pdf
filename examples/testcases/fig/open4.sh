#!/bin/sh
echo Quick, change desktop
sleep 1
test -f 1/test.pdf && xpdf -remote one -geometry 400x580+0+2 -z 90 1/test.pdf&
test -f 2/test.pdf && xpdf -remote two -geometry 400x580+400+2 -z 90 2/test.pdf&
test -f 3/test.pdf && xpdf -remote three -geometry 400x580+800+2 -z 90 3/test.pdf&
test -f 4/test.pdf && xpdf -remote four -geometry 400x580+1200+2 -z 90 4/test.pdf&
test -f 5/test.pdf && xpdf -remote five -geometry 400x580+0+582 -z 90 5/test.pdf&
test -f 6/test.pdf && xpdf -remote six -geometry 400x580+400+582 -z 90 6/test.pdf&
test -f 7/test.pdf && xpdf -remote seven -geometry 400x580+800+582 -z 90 7/test.pdf&
test -f 8/test.pdf && xpdf -remote eight -geometry 400x580+1200+582 -z 90 8/test.pdf&
sleep 1
test -f 1/test.pdf && xpdf -remote one -exec toggleOutline 
sleep 0.2
test -f 2/test.pdf && xpdf -remote two -exec toggleOutline
sleep 0.1
test -f 3/test.pdf && xpdf -remote three -exec toggleOutline
sleep 0.1
test -f 4/test.pdf && xpdf -remote four -exec toggleOutline
test -f 5/test.pdf && xpdf -remote five -exec toggleOutline
test -f 6/test.pdf && xpdf -remote six -exec toggleOutline
test -f 7/test.pdf && xpdf -remote seven -exec toggleOutline
test -f 8/test.pdf && xpdf -remote eight -exec toggleOutline
