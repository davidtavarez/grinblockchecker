# grinnode.live
### Slow script to check Grin blocks

This script will request grin node API to check every block, if a invalid block is found, a file will be created with the number of the block.

#### Running

```bash
 python main.py --protocol https --address grinnode.live --port 443 --threads 10
 ```
