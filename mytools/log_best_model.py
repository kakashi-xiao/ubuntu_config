import re
import sys
import os
import getopt
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

class_weights=[1,1,1]

def extract_train_results(infile):
    line_cnt=0

    iter_train=[]
    train_loss=[]
    loss_bbox=[]
    loss_coverage=[]
    train_outputs=[]
    while 1:
        line=infile.readline()
        line_cnt+=1
        if not line:
            break
        if line.find('sgd_solver.cpp:139')>=0: # train output

            iter_train.append(int(line.split()[5][0:-1]))
            train_loss.append(int(line.split()[5][0:-1]))
            #  print iter_test
            i=0
            train_output=[0]*20
            while(1):
                line=infile.readline();
                line_cnt+=1
                if(line.find("#")>=0):
                    train_output[i]=float(line.split()[10])
                    i+=1
                else:
                    break;
            train_outputs.append(train_output)
            loss_bbox.append(train_output[0])
            loss_coverage.append(train_output[1])
    return iter_train,train_loss,loss_bbox,loss_coverage

def extract_test_results(infile):
    line_cnt=0

    iter_train=[]
    iter_test=[]
    train_loss=[]
    test_loss=[]
    loss_bbox=[]
    loss_coverage=[]
    mAP0=[]
    mAP1=[]
    mAP2=[]
    test_outputs=[]
    while 1:
        line=infile.readline()
        line_cnt+=1
        if not line:
            break
        if line.find('solver.cpp:464')>=0: # test output
            iter_test.append(int(line.split()[5][0:-1]))
            #  print iter_test
            i=0
            test_output=[0]*20
            while(1):
                line=infile.readline();
                line_cnt+=1
                if(line.find("#")>=0):
                    test_output[i]=float(line.split()[10])
                    i+=1
                else:
                    break;
            test_outputs.append(test_output)
            loss_bbox.append(test_output[0])
            loss_coverage.append(test_output[1])
            mAP0.append(test_output[2])
            mAP1.append(test_output[3])
            mAP2.append(test_output[4])
    return iter_test,loss_bbox,loss_coverage,mAP0,mAP1,mAP2

def extract_snap_results(infile):
    line_cnt=0

    iter_snap=[]
    snap_file=[]
    loss_bbox=[]
    loss_coverage=[]
    mAP0=[]
    mAP1=[]
    mAP2=[]
    test_outputs=[]
    while 1:
        line=infile.readline()
        line_cnt+=1
        if not line:
            break
        if line.find('solver.cpp:595')>=0: # snapshot output
            snap_file.append(line.split()[9])
            while(1):
                line=infile.readline()
                line_cnt+=1
                if not line:
                    break
                if line.find('solver.cpp:464')>=0: # test output
                    iter_snap.append(int(line.split()[5][0:-1]))
                    break
            #  print iter_test
            i=0
            test_output=[0]*20
            while(1):
                line=infile.readline();
                line_cnt+=1
                if(line.find("#")>=0):
                    test_output[i]=float(line.split()[10])
                    i+=1
                else:
                    break;
            test_outputs.append(test_output)
            loss_bbox.append(test_output[0])
            loss_coverage.append(test_output[1])
            mAP0.append(test_output[2])
            mAP1.append(test_output[3])
            mAP2.append(test_output[4])
    return snap_file,iter_snap,loss_bbox,loss_coverage,mAP0,mAP1,mAP2

def MIN_loss_sum(iter_test,loss_bboxes,loss_coverages):
    if(not (len(loss_bboxes)==len(loss_coverage) )):
        print "losses lengths doesn't match"
        quit()
    else:
        best_loss_sum=10000
        best_loss=[10000]*2
        best_index=0
        for i in range(len(loss_bboxes)):
            loss_sum=loss_bboxes[i]+loss_coverages[i] 
            if(loss_sum<best_loss_sum):
                best_loss_sum=loss_sum
                best_loss=[loss_bboxes[i],loss_coverages[i]]
                best_index=i
    best_iter=iter_test[best_index]
    print "==========  Method: MIN loss_sum  ==========="
    print "best_loss:",best_loss
    print "best_index:",best_iter
    return best_loss,best_iter

def MAX_mAP_sum(iter_test,mAP0s,mAP1s,mAP2s):
    if(not (len(mAP0)==len(mAP1) and len(mAP0)==len(mAP1))):
        print "mAPs lengths doesn't match"
        quit()
    else:
        best_mAP_sum=0
        best_mAP=[0]*3
        best_index=0
        for i in range(len(mAP0s)):
            mAP_sum=mAP0[i]*class_weights[0]+mAP1[i]*class_weights[1]+mAP2[i]*class_weights[2] 
            if(mAP_sum>best_mAP_sum):
                best_mAP_sum=mAP_sum
                best_mAP=[mAP0[i],mAP1[i],mAP2[i]]
                best_index=i
    best_iter=iter_test[best_index]
    print "==========  Method: MAX mAP_sum  ==========="
    print "best_mAP:",best_mAP
    print "best_index:",best_iter
    return best_mAP,best_iter
        
if __name__ == '__main__':
    if len(sys.argv)<2:
        print """
            usage: python log_best_model.py [-t|-m] logfile1 logfile2 ..."

            -t,--target:    target stages for parameter extraction, including test|snap|train;
                            default:test

            -m,--method:    method for comparison:
                            1: MAX mAP_sum
                            2: MIN loss_sum
                            default:1
        """
        quit()

    options,args = getopt.getopt(sys.argv[1:],"t:m:",["target=","method="])
    target='test'
    method='1'
    for name,value in options:
        if name in ("-t","--target"):
            target=value
        if name in ("-m","--method"):
            method=value

    legends=['fix_mean','fix_mean2','fix','float']
    for filename in args:
        infile=open(filename)
        print "==========  Processing: "+filename+"  =========="

        if target=='train':
            pass
        elif target=='test':
            iter,loss_bbox,loss_coverage,mAP0,mAP1,mAP2=extract_test_results(infile)
        elif target=='snap':
            snap_file,iter,loss_bbox,loss_coverage,mAP0,mAP1,mAP2=extract_snap_results(infile)

        if method=='1':
            # method=1: MAX mAP_sum
            best_mAP,best_index=MAX_mAP_sum(iter,mAP0,mAP1,mAP2)
        elif method=='2':
            # method=2: MIN loss_sum
            best_mAP,best_index=MIN_loss_sum(iter,loss_bbox,loss_coverage)

