<?php
#数据库配置
$mysql_server_name='127.0.0.1';    
$mysql_username='mail_report';  
$mysql_password='mail_report';  
$mysql_database='mail_report'; 
$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password,$mysql_database);
mysql_query("set names 'utf8'");
#$sql='select send_time,mail_id,mail_addr,server_domain,server_ip,mail_status from real_mail_log where send_time>curdate()-1 order by send_time desc limit 50';
#$sql='select send_time,mail_id,mail_addr,server_domain,server_ip,mail_status from real_mail_log limit 10';
$sql='select send_time,mail_id,send_mail_addr,recv_mail_addr,server_domain,server_ip,client_ip,mail_status,file_name from real_mail_log limit 10';
//mysql_query($sql);
//mysql_set_charset("UTF8",$conn); 
mysql_select_db($mysql_database,$conn);    
$result=mysql_query($sql,$conn);  
#echo $result;
$resultq=mysql_query($query,$conn);  
//mysql_close($conn);   
echo "<table align=center><tr><td><font size=6>"."邮件发送状态查询"."</front></td></tr></table>" ;
echo "&nbsp";
$acceptmail = trim($_POST['acceptmail']);
$sendmail = trim($_POST['sendmail']);
$st = $_POST['st'];
$et = $_POST['et'];
$zf = '%';
echo 'st'.$st;
echo "<br />";
echo 'et'.$et;
echo "<br />";
echo 'accmail:'.$acceptmail;
echo 'sendmail:'.$sendmail;
if ($st != null or $et != null )
{
    if ($acceptmail == null and $sendmail == null)
    {
	    $query = 'select send_time,mail_id,send_mail_addr,recv_mail_addr,server_domain,server_ip,client_ip,mail_status,file_name from real_mail_log where Date(send_time) >='.'\''.$st.'\''.' and Date(send_time) <='.'\''.$et.'\''.' order by send_time desc';
    }
    else if ($sendmail != null and $acceptmail !==null)
    {
	    $query = 'select send_time,mail_id,send_mail_addr,recv_mail_addr,server_domain,server_ip,client_ip,mail_status,file_name from real_mail_log where (Date(send_time) >='.'\''.$st.'\''.' and Date(send_time)<='.'\''.$et.'\''.') and send_mail_addr like '.'\''.$zf.$sendmail.$zf.'\' and recv_mail_addr like '.'\''.$zf.$acceptmail.$zf.'\' order by send_time desc';
    }
    else if ($acceptmail == null and $sendmail != null)
    {
	    $query = 'select send_time,mail_id,send_mail_addr,recv_mail_addr,server_domain,server_ip,client_ip,mail_status,file_name from real_mail_log where (Date(send_time) >='.'\''.$st.'\''.' and Date(send_time)<='.'\''.$et.'\''.') and send_mail_addr like '.'\''.$zf.$sendmail.$zf.'\' order by send_time desc';
    }
    else
    {
 	    $query = 'select send_time,mail_id,send_mail_addr,recv_mail_addr,server_domain,server_ip,client_ip,mail_status,file_name from real_mail_log where (Date(send_time) >='.'\''.$st.'\''.' and Date(send_time)<='.'\''.$et.'\''.') and recv_mail_addr like '.'\''.$zf.$acceptmail.$zf.'\' order by send_time desc';
    }

$resultq=mysql_query($query,$conn);
}
//echo $query." ";
//echo $acceptmail.$st.$et;

//查询条件
echo "<script type='text/javascript' src='./showdate.js'></script>";
?>
<form action="<?php echo $_SERVER['PHP_SELF'];?>" method="post">
<table align=center>
<tr><td>发件者邮件地址：<input type='text' value='<?php echo $_POST['sendmail'];?>'name='sendmail' style='width:180;' /></td></tr>
<tr><td>收件者邮件地址：<input type='text' value='<?php echo $_POST['acceptmail'];?>'name='acceptmail' style='width:180;' /></td></tr>
<tr><td>邮件发送时间段：<input type='text' id='st' name='st' onclick="return Calendar('st');" value='<?php echo $_POST['st'];?>' class='text' style='width:85px;'/>
-<input type='text' id='et' onclick="return Calendar('et');" value='<?php echo $_POST['et'];?>' name='et' class='text' style='width:85px;'/>
 <input type="submit" name="submit" value="查询" style='width:50px;'> 
 </td></tr>
</table></form>
<br>
<table align=center>
<?php
echo "<tr>"; 
while($field = mysql_fetch_field($result)){//使用while输出表头
	if ($field->name=="mail_id") 
	{
	    echo "<td>&nbsp;"."邮件ID"."&nbsp;</td>";  }

	if ($field->name=="send_time") 
	{
	    echo "<td>&nbsp;"."发送时间"."&nbsp;</td>";  }

	if ($field->name=="send_mail_addr")
        {
            echo "<td>&nbsp;"."发件者邮件地址"."&nbsp;</td>";  }

 	if ($field->name=="recv_mail_addr")
        {
            echo "<td>&nbsp;"."收件者邮件地址"."&nbsp;</td>";  }

	if ($field->name=="server_domain") 
	{
	    echo "<td>&nbsp;"."收件服务器域名"."&nbsp;</td>";  }

	if ($field->name=="server_ip") 
	{
	    echo "<td>&nbsp;"."收件服务器IP"."&nbsp;</td>";  }

	if ($field->name=="client_ip") 
	{
	    echo "<td>&nbsp;"."收件服务器IP"."&nbsp;</td>";  }

	if ($field->name=="mail_status") 
	{
	    echo "<td>&nbsp;"."邮件发送状态"."&nbsp;</td>";  }

	if ($field->name=="file_name") 
	{
	    echo "<td>&nbsp;"."文件名"."&nbsp;</td>";  }

 }  

echo "</tr>";
  
#提交后处理
if($_POST['submit'])
{
  $flag = 0;
//按查询条件输出结果
	while($rows = mysql_fetch_row($resultq))
	{//使用while遍历所有记录，并显示在表格的tr中
		echo "<tr bgcolor=#CC9999>";
		for($i = 0; $i < count($rows); $i++)
 		echo "<td>&nbsp;".$rows[$i]."</td>";
             $flag++;
	}
	echo "</tr></table>";
        if ($flag == 0)
        echo "<table align=center bgcolor=#cc3366 >没有找到合适的记录</table>";
}
else
{

//默认输出结果
	while($rows = mysql_fetch_row($result)){
	//使用while遍历所有记录，并显示在表格的tr中  
		echo "<tr bgcolor=#CC9999>";  
		for($i = 0; $i < count($rows); $i++)  
 		echo "<td>&nbsp;".$rows[$i]."</td>";  
	}  
	echo "</tr></table>"; 
}


?>
