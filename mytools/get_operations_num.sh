#!/bin/bash
set -e

export PYTHONPATH=/home/shengxiao/workspace/prune_tool/python
echo $#
if [ $# -lt 2 ]
then
    echo "usage: ./get_opt.sh [final_model] [train_prototxt]"
else
    
    final_model=$1
    train_proto=$2
    bname=`basename $1 | awk -F '.' '{print $1}'`
    transformed_model=${1}"_transformed"
    final_proto=`dirname $1`"/"${bname}".prototxt"
    transformed_proto=`dirname $1`"/"${bname}".prototxt_transformed"
    echo $bname
    echo $transformed_model
    echo $final_proto
    echo $transformed_proto

    /home/shengxiao/workspace/prune_tool_class2/build/tools/transform_prune_model $final_model $transformed_model

    /home/shengxiao/workspace/prune_tool_class2/build/tools/binary_to_text $transformed_model $final_proto --remove_blobs --remove_split

    # /home/shengxiao/workspace/caffe_prune/build/tools/convert_net_proto_text_deploy2test $final_proto $train_proto $transformed_proto
    cp $final_proto $transformed_proto
    # sed -i '/stage: "val"/d' $transformed_proto
    sed -i '/TRAIN/d' $transformed_proto
    sed -i '/batch_size/s/4/1/g' $transformed_proto
    
    /home/shengxiao/workspace/prune_tool_class2/build/tools/get_operations_num $transformed_proto

fi
