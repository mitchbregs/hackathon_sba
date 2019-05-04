from Payment import *

authdotnet = Payment()

print ( authdotnet.send('370000000000002', '2020-12', '2.22') )
print ( authdotnet.send('6011000000000012', '2020-12', '99.99') )
print ( authdotnet.send('5424000000000015', '2020-12', '2.22') )

import pdb; pdb.set_trace()
