def ch4(fs, dt, N, fmin, fmax, tmax, tmin, wf, vm, dBvalve, plotres, TimeFrequency, dataharvest, complexdiag,
        Timedomain, ch0instru, ch1instru, ch2instru, ch3instru, limtxset1, limtxset2, limtxset3, limtxset4,
        microphonechannel, filepath, plotpath, filetype):

    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import signal
    import datetime
    import matplotlib as mpl

    mpl.rcParams['agg.path.chunksize'] = 10000
    start = datetime.datetime.now()

    filelist=os.listdir(filepath)
    for i in filelist:
        if i =='.DS_Store':
            filelist.remove('.DS_Store')
            break
    m= len(filelist)

    filename=[]
    for i in range (0,m):
        name=filelist[i]
        name=name[0:-4]
        filename.append(name)

    ######讀入信號資訊並繪圖
    for info, name in zip(filelist, filename):
        print('start '+str(name)+' data extract.')
        domain = os.path.abspath(filepath)
        file = os.path.join(domain,info)
        if filetype=='csv':
            locals()[name]=pd.read_csv(file)
            name1=str(name)+str(ch0instru)
            locals()[name1]=locals()[name].iloc[:, 1].values
            name2=str(name)+str(ch1instru)
            locals()[name2]=locals()[name].iloc[:, 2].values
            name3=str(name)+str(ch2instru)
            locals()[name3]=locals()[name].iloc[:, 3].values
            name4=str(name)+str(ch3instru)
            locals()[name4]=locals()[name].iloc[:, 4].values
        if filetype=='txt':
            file=open(file)
            element = []
            for line in file:
                element.append(line)
            l = len(element)
            MeasDOF = []
            for i in range(0, l):
                str1 = element[i]
                strb = str1.strip('\n')
                strc = strb.split('\t')
                MeasDOF.append(strc)
            MeasDOF = np.array(MeasDOF)
            c = np.zeros((l, 5))
            for i in range(0, 5):
                for j in range(0, l):
                    d = MeasDOF[j, i]
                    d = float(d)
                    c.itemset((j, i), d)
            locals()[name] = c
            name1 = str(name) + str(ch0instru)
            locals()[name1] =locals()[name][:,1]
            name2 = str(name) + str(ch1instru)
            locals()[name2] = locals()[name][:,2]
            name3 = str(name) + str(ch2instru)
            locals()[name3] = locals()[name][:,3]
            name4 = str(name) + str(ch3instru)
            locals()[name4] = locals()[name][:,4]
        l=len(locals()[name1])
        time = dt * np.array(range(l))
        print('time length: '+str(time[-1]))
        if microphonechannel==1:
            mic=locals()[name2]
            other1=locals()[name1]
            other2=locals()[name3]
            other3=locals()[name4]
            A=name2
            B=name1
            C=name3
            D=name4

        elif microphonechannel==2:
            mic=locals()[name3]
            other1=locals()[name1]
            other2=locals()[name2]
            other3=locals()[name4]
            A = name3
            B = name1
            C = name2
            D = name4

        elif microphonechannel==3:
            mic = locals()[name4]
            other1=locals()[name1]
            other2=locals()[name2]
            other3=locals()[name3]
            A = name4
            B = name1
            C = name2
            D = name3

        else:
            mic=locals()[name1]
            other1=locals()[name2]
            other2=locals()[name3]
            other3=locals()[name4]
            A = name1
            B = name2
            C = name3
            D = name4

        skip=0
        overdBvalve=0
        labelt=[]
        labelf=[]
        freqlist=np.array([0])
        Timelist = np.array([0])
        SPL=np.array([0])

    #####利用短時傅立葉進行信號處理，並將計算結果以熱點圖呈現
        f, t, Zxx = signal.stft(mic, fs, window=wf, nperseg=N)
        f, t, Zxx1 = signal.stft(other1, fs, window=wf, nperseg=N)
        f, t, Zxx2 = signal.stft(other2, fs, window=wf, nperseg=N)
        f, t, Zxx3 = signal.stft(other3, fs, window=wf, nperseg=N)
        a = np.abs(Zxx)
        b = 10 * np.log(a / (20 * 10 ** -6))
        r=len(b)
        o=np.size(a,1)
        for i in range(100,r):
            for j in range(0,o):
                check=b[i,j]
                if check>dBvalve:
                    labelt.append(j)
                    labelf.append(i)
                    SPL=np.vstack((SPL,check))
                    overdBvalve=1
                    if TimeFrequency == 1:
                        if skip==0:
                            plt.figure(figsize=(8, 6), dpi=plotres)
                            cm = plt.cm.get_cmap('binary')
                            plt.pcolormesh(t, f, b, cmap=cm, vmin=0, vmax=vm)
                            plt.xticks(fontproperties='Times New Roman', fontsize=16)
                            plt.yticks(fontproperties='Times New Roman', fontsize=16)
                            plt.ylim(fmin, fmax)
                            if tmax > 0:
                                plt.xlim(tmin, tmax)
                            plt.title('STFT Magnitude', fontdict={'family': 'Times New Roman', 'size': 24})
                            plt.ylabel('Frequency [Hz]', fontdict={'family': 'Times New Roman', 'size': 20})
                            plt.xlabel('Time [sec]', fontdict={'family': 'Times New Roman', 'size': 20})
                            plt.colorbar()
                            plt.savefig(plotpath+'/'+str(A)+'_STFT',dpi=600, bbox_inches="tight")
                            plt.close('all')

                            a = np.abs(Zxx1)
                            plt.figure(figsize=(8, 6), dpi=plotres)
                            cm = plt.cm.get_cmap('binary')
                            plt.pcolormesh(t, f, a, cmap=cm, vmin=0)
                            plt.xticks(fontproperties='Times New Roman', fontsize=16)
                            plt.yticks(fontproperties='Times New Roman', fontsize=16)
                            if tmax > 0:
                                plt.xlim(tmin, tmax)
                            plt.ylim(fmin, fmax)
                            plt.title('STFT Magnitude', fontdict={'family': 'Times New Roman', 'size': 24})
                            plt.ylabel('Frequency [Hz]', fontdict={'family': 'Times New Roman', 'size': 20})
                            plt.xlabel('Time [sec]', fontdict={'family': 'Times New Roman', 'size': 20})
                            plt.colorbar()
                            plt.savefig(plotpath + '/' + str(B)+'_STFT', dpi=600, bbox_inches="tight")
                            plt.close('all')

                            a = np.abs(Zxx2)
                            plt.figure(figsize=(8, 6), dpi=plotres)
                            cm = plt.cm.get_cmap('binary')
                            plt.pcolormesh(t, f, a, cmap=cm, vmin=0)
                            plt.xticks(fontproperties='Times New Roman', fontsize=16)
                            plt.yticks(fontproperties='Times New Roman', fontsize=16)
                            if tmax > 0:
                                plt.xlim(tmin, tmax)
                            plt.ylim(fmin, fmax)
                            plt.title('STFT Magnitude', fontdict={'family': 'Times New Roman', 'size': 24})
                            plt.ylabel('Frequency [Hz]', fontdict={'family': 'Times New Roman', 'size': 20})
                            plt.xlabel('Time [sec]', fontdict={'family': 'Times New Roman', 'size': 20})
                            plt.colorbar()
                            plt.savefig(plotpath + '/'+str(C)+'_STFT', dpi=600, bbox_inches="tight")
                            plt.close('all')

                            a = np.abs(Zxx3)
                            plt.figure(figsize=(8, 6), dpi=plotres)
                            cm = plt.cm.get_cmap('binary')
                            plt.pcolormesh(t, f, a, cmap=cm, vmin=0)
                            plt.xticks(fontproperties='Times New Roman', fontsize=16)
                            plt.yticks(fontproperties='Times New Roman', fontsize=16)
                            if tmax > 0:
                                plt.xlim(tmin, tmax)
                            plt.ylim(fmin, fmax)
                            plt.title('STFT Magnitude', fontdict={'family': 'Times New Roman', 'size': 24})
                            plt.ylabel('Frequency [Hz]', fontdict={'family': 'Times New Roman', 'size': 20})
                            plt.xlabel('Time [sec]', fontdict={'family': 'Times New Roman', 'size': 20})
                            plt.colorbar()
                            plt.savefig(plotpath + '/' + str(D) + '_STFT', dpi=600, bbox_inches="tight")
                            plt.close('all')

                            skip=1
                            print(str(name) + 'STFT plot is output to direct ' + plotpath)

        if dataharvest==1:
            if overdBvalve==1:
                for i, j in zip(labelf, labelt):
                    freq = f[i]
                    freqlist = np.vstack((freqlist, freq))
                    timecode = t[j]
                    Timelist = np.vstack((Timelist, timecode))
                freqlist = np.delete(freqlist, 0)
                Timelist = np.delete(Timelist, 0)
                SPL = np.delete(SPL, 0)
                SPLdB = np.vstack((freqlist, SPL))
                SPLdB = np.vstack((SPLdB, Timelist))
                SPLdB = SPLdB.T
                np.savetxt(plotpath + '/' + str(A), SPLdB, fmt='%f', delimiter='\t',
                           header='Frequency (Hz)\tSPL (dB)\tTime (s)', comments='')
                print(str(name) + '.txt is output to direct ' + plotpath)

        if complexdiag == 1:
            if len(labelt):
                limtx = 1.1 * (np.max(np.absolute(np.real(Zxx[:, i]))))
                plt.figure(figsize=(8, 6), dpi=plotres)
                for i in labelt:
                    plt.scatter(np.real(Zxx[:,i]), f, c='k')
                plt.xticks(fontproperties='Times New Roman', fontsize=16)
                plt.yticks(fontproperties='Times New Roman', fontsize=16)
                plt.ylim(fmin, fmax)
                if limtxset1 > 0:
                    plt.xlim(-limtxset1, limtxset1)
                else:
                    plt.xlim(-limtx, limtx)
                plt.title('Instability Diagram', fontdict={'family': 'Times New Roman', 'size': 24})
                plt.ylabel('Frequency [Hz]', fontdict={'family': 'Times New Roman', 'size': 20})
                plt.xlabel('Instability [-]', fontdict={'family': 'Times New Roman', 'size': 20})
                plt.savefig(plotpath + '/' + str(A)+'_ID', dpi=600, bbox_inches="tight")
                plt.close('all')

                limtx = 1.1 * (np.max(np.absolute(np.real(Zxx1[:, i]))))
                plt.figure(figsize=(8, 6), dpi=plotres)
                for i in labelt:
                    plt.scatter(np.real(Zxx1[:, i]), f, c='c')
                plt.xticks(fontproperties='Times New Roman', fontsize=16)
                plt.yticks(fontproperties='Times New Roman', fontsize=16)
                plt.ylim(fmin, fmax)
                if limtxset2 > 0:
                    plt.xlim(-limtxset2, limtxset2)
                else:
                    plt.xlim(-limtx, limtx)
                plt.title('Instability Diagram', fontdict={'family': 'Times New Roman', 'size': 24})
                plt.ylabel('Frequency [Hz]', fontdict={'family': 'Times New Roman', 'size': 20})
                plt.xlabel('Instability [-]', fontdict={'family': 'Times New Roman', 'size': 20})
                plt.savefig(plotpath + '/' + str(B)+'_ID', dpi=600, bbox_inches="tight")
                plt.close('all')

                limtx = 1.1 * (np.max(np.absolute(np.real(Zxx2[:, i]))))
                plt.figure(figsize=(8, 6), dpi=plotres)
                for i in labelt:
                    plt.scatter(np.real(Zxx2[:, i]), f, c='m')
                plt.xticks(fontproperties='Times New Roman', fontsize=16)
                plt.yticks(fontproperties='Times New Roman', fontsize=16)
                plt.ylim(fmin, fmax)
                if limtxset3 > 0:
                    plt.xlim(-limtxset3, limtxset3)
                else:
                    plt.xlim(-limtx, limtx)
                plt.title('Instability Diagram', fontdict={'family': 'Times New Roman', 'size': 24})
                plt.ylabel('Frequency [Hz]', fontdict={'family': 'Times New Roman', 'size': 20})
                plt.xlabel('Instability [-]', fontdict={'family': 'Times New Roman', 'size': 20})
                plt.savefig(plotpath + '/' + str(C)+'_ID', dpi=600, bbox_inches="tight")
                plt.close('all')

                limtx = 1.1 * (np.max(np.absolute(np.real(Zxx3[:, i]))))
                plt.figure(figsize=(8, 6), dpi=plotres)
                for i in labelt:
                    plt.scatter(np.real(Zxx2[:, i]), f, c='m')
                plt.xticks(fontproperties='Times New Roman', fontsize=16)
                plt.yticks(fontproperties='Times New Roman', fontsize=16)
                plt.ylim(fmin, fmax)
                if limtxset4 > 0:
                    plt.xlim(-limtxset4, limtxset4)
                else:
                    plt.xlim(-limtx, limtx)
                plt.title('Instability Diagram', fontdict={'family': 'Times New Roman', 'size': 24})
                plt.ylabel('Frequency [Hz]', fontdict={'family': 'Times New Roman', 'size': 20})
                plt.xlabel('Instability [-]', fontdict={'family': 'Times New Roman', 'size': 20})
                plt.savefig(plotpath + '/' + str(D) + '_ID', dpi=600, bbox_inches="tight")
                plt.close('all')
                print(str(name) + 'Instability plot is output to direct ' + plotpath)

        if Timedomain==1:
            plt.figure(figsize=(8, 6), dpi=plotres)
            plt.plot(time, x)
            plt.xticks(fontproperties='Times New Roman', fontsize=16)
            plt.yticks(fontproperties='Times New Roman', fontsize=16)
            plt.xlim(0,10)
            plt.title('Time  Magnitude', fontdict={'family': 'Times New Roman', 'size': 24})
            plt.ylabel('Magnitude [-]', fontdict={'family': 'Times New Roman', 'size': 20})
            plt.xlabel('Time [sec]', fontdict={'family': 'Times New Roman', 'size': 20})
            plt.savefig(plotpath+'/t'+str(name),dpi=600, bbox_inches="tight")
            plt.close('all')

            print(str(name) + 'Timedomain plot is output to direct ' + plotpath)


        print(str(name)+' data extract done!!')
        del (locals()[name])
        del (locals()[name1])
        del (locals()[name2])
        del (locals()[name3])
        del (locals()[name4])

    end = datetime.datetime.now()
    print('Estimate time', end - start)