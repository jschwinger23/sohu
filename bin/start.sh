cur_dir=$(cd $(dirname $0) && pwd)
source $cur_dir/env.sh
python $cur_dir/../src/run.py
