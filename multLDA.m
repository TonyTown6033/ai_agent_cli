load('data.txt');                      %data.txt为存储训练集的文件

j=1;k=1; h=size(data);h=h(1,1);        %将数据进行分类 data1为含有特征物质的数据
for i=1:h                              %data2为不含有特征物质的数据
    if data(i,8)==1
        data1(j,1:7)=data(i,1:7);
        j=j+1;
    else
        data2(k,1:7)=data(i,1:7);
        k=k+1;
    end
end

n1=size(data1);n1=n1(1,1);             %通过训练集的数据来得到参数m1,m2,s1,s2的值
n2=size(data2);n2=n2(1,1);
sum1=0;sum2=0;
for i=1:n1
    sum1=sum1+data1(i,:);
end
for j=1:n2
    sum2=sum2+data2(j,:);
end

m1=sum1/n1;m1=m1.';                     %得到m1,m2
m2=sum2/n2;m2=m2.';

s1=zeros(7,7);s2=zeros(7,7);            %有7个指标，所以类内见矩阵为7阶方阵
for i=1:n1
    s1=s1+(data1(i,:).'-m1)*(data1(i,:).'-m1).';
end

for j=1:n2
    s2=s2+(data2(j,:).'-m2)*(data2(j,:).'-m2).';
end                                     %得到s1,s2的数据

w=inv((s1+s2))*(m1-m2);                  %计算w和b的值
b=-0.5*w.'*(m1+m2);

for i=1:19999                             %利用判断函数来导出判别结果存储到矩阵A中
    A(i)=data(i,1:7)*w+b;
   if A(i)>0
        A(i)=1;
    else
        A(i)=0;
    end
end

data(:,9)=A.';                            %与测试集进行比较，得出正确率

u=0;
for i=1:19999
    if data(i,8)~=data(i,9)
        u=u+1;
    end
end

1-u/19999                                   %输出正确率

load('test.txt');
p=size(test);p=p(1,1);                      %预测
for i=1:p
    B(i)=test(i,1:7)*w+b;
   if B(i)>0
        B(i)=1;
    else
        B(i)=0;
    end
end

test(:,8)=B.';
test
