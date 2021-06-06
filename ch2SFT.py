def ch2(fs, dt, N, fmin, fmax,tmax ,tmin ,wf , vm, dBvalve, plotres, TimeFrequency, dataharvest, complexdiag, Timedomain,
                       ch0instru, ch1instru, limtxset1, limtxset2, microphonechannel, filepath, plotpath,filetype):
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import signal
    import datetime
    import matplotlib as mpl

    mpl.rcParams['agg.path.chunksize'] = 10000
    start = datetime.datetime.now()                                                                                         #開始記錄時間

    #####從指定位置取得量測到的所有信號CSV檔
    #####在指定路徑中，調出資料夾中所有的檔案名稱(包含副檔名)，並建立為一個list
    filelist=os.listdir(filepath)                                                                                           #從指定路徑讀取所有檔案名稱
    for i in filelist:                                                                                                      #檢查欲讀取之資料中，是否有存在DS_Store檔
        if i =='.DS_Store':
            filelist.remove('.DS_Store')                                                                                    #由於MAC會有.DS_Store快取檔，需要先移除此快取檔才可順利讀取所有檔案，若無此快取檔則無需此指令
            break
    m= len(filelist)                                                                                                        #讀取list中的項目數目，目的用來將list中的檔案名稱重新命名為資料所用

    #####以下為重新命名list中的名稱，之後用以命名匯入之信號
    filename=[]                                                                                                             #建立一空list
    for i in range (0,m):
        name=filelist[i]                                                                                                    #依序呼叫filelist中的所有檔案名稱
        name=name[0:-4]                                                                                                     #將欲作為名稱之文字擷取出來
        filename.append(name)                                                                                               #將擷取出的文字置入新建的list

    ######讀入信號資訊並繪圖
    for info, name in zip(filelist, filename):
        print('start '+str(name)+' data extract.')
        domain = os.path.abspath(filepath)                                                                                  #指定文件夾之路徑
        file = os.path.join(domain,info)                                                                                    #將文件夾路徑及檔案名稱拼湊為完整路
        if filetype=='csv':
            locals()[name]=pd.read_csv(file)                                                                                    #讀取指定位置之CSV檔
            name1=str(name)+str(ch0instru)
            locals()[name1]=locals()[name].iloc[:, 1].values                                                                     #由於在此僅使用單一channal進行檔案擷取，在此只擷取ch0之信號，若實驗有需要多頻道擷取數據，則需要增加擷取不同的列
            name2=str(name)+str(ch1instru)
            locals()[name2]=locals()[name].iloc[:, 2].values
        if filetype=='txt':
            file = open(file)
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
            locals()[name1] = locals()[name][:,1]
            name2 = str(name) + str(ch1instru)
            locals()[name2] = locals()[name][:,2]
        l=len(locals()[name1])                                                                                               #計算資料中總資料點s
        time = dt * np.array(range(l))                                                                                      #建立資料量測的時間序列
        print('time length: '+str(time[-1]))                                                                                #輸出資料量測總時長
        if microphonechannel==1:
            mic=locals()[name2]                                                                                                  #將擷取出來的資料定義為ch0
            A=name2
            other1=locals()[name1]
            B=name1
        else:
            mic=locals()[name1]
            A=name1
            other1=locals()[name2]
            B=name2
        skip=0                                                                                                              #因為同一個檔案中，高於閥值之參數可能高於1個，因此設定一開關。若此時間段(信號)已輸出過，此參數即修改為1，之後則不重複出圖
        overdBvalve=0                                                                                                       #確認有超過閥值之聲壓級，以利後續輸出txt檔
        labelt=[]                                                                                                           #將發生最大聲壓級的時間位置記錄在此list中
        labelf=[]                                                                                                           #將發生最大聲壓級的頻率位置記錄在此list中
        freqlist=np.array([0])                                                                                              #將發生最大聲壓級的頻率記錄在此array中
        Timelist = np.array([0])
        SPL=np.array([0])                                                                                                   #將最大聲壓級記錄在此array中

    #####利用短時傅立葉進行信號處理，並將計算結果以熱點圖呈現
        f, t, Zxx=signal.stft(mic, fs,window =wf, nperseg=N)                                                                           #輸入資料為x(時域信號) 及 fs(取樣頻率)，計算結果包含了t(時間)、f(頻率)及Zxx(幅值)
        f, t, Zxx1=signal.stft(other1, fs,window =wf, nperseg=N)
        a = np.abs(Zxx)                                                                                                     #由於計算結果中包含了實部及虛部，因此將信號取絕對值，得到當下之幅值
        b = 10 * np.log(a / (20 * 10 ** -6))                                                                                #在此輸入信號為聲壓信號，因此將其轉換為dB
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
                            plt.savefig(plotpath + '/' + str(B)+'_STFT', dpi=plotres, bbox_inches="tight")
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
                limtx=1.1*(np.max(np.absolute(np.real(Zxx[:, i]))))
                plt.figure(figsize=(8, 6), dpi=plotres)
                for i in labelt:
                    plt.scatter(np.real(Zxx[:,i]), f, c='k')
                plt.xticks(fontproperties='Times New Roman', fontsize=16)
                plt.yticks(fontproperties='Times New Roman', fontsize=16)
                plt.ylim(fmin, fmax)
                if limtxset1>0:
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
                plt.savefig(plotpath + '/' + str(B) + '_ID', dpi=600, bbox_inches="tight")
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
            plt.savefig(plotpath+'/t'+str(A),dpi=600, bbox_inches="tight")
            plt.close('all')
            print(str(name) + 'Timedomain plot is output to direct ' + plotpath)


        print(str(name)+' data extract done!!')
        del (locals()[name])
        del (locals()[name1])
        del (locals()[name2])

    end = datetime.datetime.now()
    print('Estimate time', end - start)