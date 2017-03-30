import re
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

if __name__ == '__main__':
    n_figure=0
    if len(sys.argv)>=2:
        files=sys.argv[1:]
    else:
        files="log1.txt"
    for filename in files:
        print "==========  Processing "+filename+str(n_figure)+"  =================="
        file=open(filename)
        cnt=0
        n_figure+=1
        iter_train=list()
        iter_test=list()
        train=list()
        test=list()
        accuracy1=list()
        accuracy5=list()
        flag=0
        while 1:
            line=file.readline()
            #  print "==========  Processing "+str(cnt)+"  =================="
            #  print "==========  Processing "+line+"  =================="
            if not line:
                break
            index1=line.find('Iteration')
            if index1>=0:
                index2=line.find('loss')
                if index2>=0:
                    nums=re.findall(r"\d+\.?\d*",line[index1:])
                    iter=int(nums[0])
                    loss=float(nums[1])
                    iter_train.append(iter)
                    train.append(loss)
                index3=line.find('Testing net')
                if index3>=0:
                    nums=re.findall(r"\d+\.?\d*",line[index1:])
                    iter=int(nums[0])
                    iter_test.append(iter)
                    
                    line = file.readline()
                    #  index=line.find('accuracy_top1')
                    index=line.find('mAP-class0')
                    while (index<0):
                        line = file.readline()
                        #  index=line.find('accuracy_top1')
                        index=line.find('mAP-class0')
                        #  print "==========  Processing "+line+"  =================="
                        #  print "=======10==========="
                        #  raw_input("input2:")
                        flag+=1
                        if flag>=10:
                            flag=0
                            print "=======No Data==========="
                            break
                    nums=re.findall(r"\d+\.?\d*",line[index:])
                    if not nums:
                        top1=accuracy1[-1]
                    else:
                        top1=float(nums[1])
                    accuracy1.append(top1)

                    line = file.readline()
                    index=line.find('mAP-class1')
                    while (index<0):
                        line = file.readline()
                        #  index=line.find('accuracy_top5')
                        index=line.find('mAP-class1')
                        flag+=1
                        if flag>=10:
                            flag=0
                            print "=======No Data==========="
                            break
                    nums=re.findall(r"\d+\.?\d*",line[index:])
                    if not nums:
                        top5=accuracy5[-1]
                    else:
                        top5=float(nums[1])
                    accuracy5.append(top5)

                    line = file.readline()
                    index=line.find('loss')
                    while (index<0):
                        line = file.readline()
                        index=line.find('loss')
                        flag+=1
                        if flag>=10:
                            flag=0
                            print "=======No Data==========="
                            break
                    nums=re.findall(r"\d+\.?\d*",line[index:])
                    if not nums:
                        top_loss=0
                    else:
                        top_loss=float(nums[0])
                    #accuracy.append(top_loss)
                    #test.append(accuracy)

                    #print "Iteration = %s: top1 = %f; top5 = %f; top_loss = %f "%(iter,top1,top5,top_loss)


            cnt+=1
            #  if cnt>=50000:
                #  break
        '''
        for i in range(1,len(iter_train)):
            print "iteration = %s; loss = %f "%(iter_train[i],train[i])
        for i in range(1,len(iter_test)):
            accuracy=test[i]
            print "Iteration = %s: top1 = %f; top5 = %f; top_loss = %f "%(iter_test[i],accuracy[0],accuracy[1],accuracy[2])
'''
        if accuracy1 and accuracy5 and train:
            print "==========  Latest Result:Acc1: "+str(accuracy1[-1])+" Acc5: "+str(accuracy5[-1])+"  =================="
        else:
            print "No Data"
            break
        print n_figure
        plt.figure(n_figure)
        ax1 = plt.subplot(2,1,1)
        ax2 = plt.subplot(2,1,2)

        x = np.linspace(0,1,100)
        plt.sca(ax1)
        plt.plot(iter_train,train)
        plt.sca(ax2)
        plt.plot(iter_test,accuracy1)
        plt.figure(10)
        plt.plot(iter_test,accuracy1,label=filename)
        plt.legend(loc='upper left')
        plt.figure(11)
        plt.plot(iter_test,accuracy5,label=filename)
        plt.legend(loc='upper left')
    plt.show()
while 1:
    n=raw_input("Press 'q' to exit")
    if n=='q':
        break
