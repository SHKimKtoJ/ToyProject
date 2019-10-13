<?php
/*
봇에서 요청하는 버스정보를 처리.
*/


/*
//xml을 json으로 변환하는 예제. 내부 값이 사라지는 현상 해결 필요
class XmlToJsonConverter{
    public function ParseXML($url){
        $fileContents = file_get_contents($url);
        $fileContents = str_replace(array("\n", "\r", "\t"),'',$fileContents);  //tabs,newline 등 제거
        $fileContents = trim(str_replace('"',"'",$fileContents));   //quotation mark, apostrophe 제거
        $myXml = simplexml_load_string($fileContents);
        $json = json_encode($myXml);
        return $json;
    }
}
//XML file Path
$url='http://openapi.changwon.go.kr/rest/bis/BusArrives/?ServiceKey=qj9in7MQl0zJbAx185AyjJX1lu9r1a0r24DbUg0uEuT9C0iK%2Fge9JYvwdFInIGaEXL3nUX8NqVUnwNOpZdFKEQ%3D%3D&station=379000591';
//임시로 창원대학교종점 정류장 정보를 넣어봄.

$jsonObj = new XmlToJsonConverter();
$myjson = $jsonObj -> ParseXML($url);
print_r($myjson);
*/
    $ch = curl_init();
    
    if($_GET['busNo'] == null){
        $getURL = "http://openapi.changwon.go.kr/rest/bis/BusArrives/?ServiceKey=qj9in7MQl0zJbAx185AyjJX1lu9r1a0r24DbUg0uEuT9C0iK%2Fge9JYvwdFInIGaEXL3nUX8NqVUnwNOpZdFKEQ%3D%3D&station=".$_GET['station'];
    }else{
        $getURL = "http://openapi.changwon.go.kr/rest/bis/ArriveInfo/?ServiceKey=qj9in7MQl0zJbAx185AyjJX1lu9r1a0r24DbUg0uEuT9C0iK%2Fge9JYvwdFInIGaEXL3nUX8NqVUnwNOpZdFKEQ%3D%3D&station=".$_GET['station']."&route=".$_GET['busNo'];
    }
    curl_setopt($ch, CURLOPT_URL, $getURL);
    
    
    
    curl_setopt($ch, CURLOPT_URL,$getURL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	$outCurlBus = curl_exec($ch);
	$pattern = '/(\<!\[CDATA\[)(.+)(\]\]\>)/x';
    $replacement = '$2';
    $afterParse = preg_replace($pattern, $replacement, $outCurlBus);
	$arrBus = simplexml_load_string($afterParse);
    $arrBus = json_encode($arrBus,true);
    $arrBus = json_decode($arrBus, true);
    //print_r(array_keys($arrBus));
    //echo "<br> \n";
    //print_r(array_keys($arrBus['MsgBody']));
    //echo "<br> \n";
    //print_r(array_keys($arrBus['MsgBody']['ArriveInfoList']));
    //echo "<br> \n";
    //print_r(array_keys($arrBus['MsgBody']['ArriveInfoList']['row']));
    //echo "<br> \n";
    //어레이 구조를 보기 위한 예제코드.
    $num = $arrBus['MsgBody']['ArriveInfoList']['row'][0]["ROUTE_ID"];
    $arrNum = str_split($num);
    //print_r($arrNum);
    $sliArrNum = array_slice($arrNum, 5);
    $getSta = $_GET['station'];
    $getBusNo = $_GET['busNo'];

    //$preTime = intval($arrBus['MsgBody']['ArriveInfoList']['row']['PREDICT_TRAV_TM']);
    
    
    if(($getSta != null)&&($getBusNo == null)){
        $cntRowArrBus = count($arrBus['MsgBody']['ArriveInfoList']['row']);
        for($i = 0; $i < $cntRowArrBus ; $i++){
            //ROUTE_ID에서 필요한 부분만 선택. ex> 379001000 > 100, 379000600 > 60 등.
            $num1 = $arrBus['MsgBody']['ArriveInfoList']['row'][$i]["ROUTE_ID"];
            $arrNum = str_split($num1);
            $sliArrNum = array_slice($arrNum, 5);
            $n1 = $sliArrNum[0];
            $n2 = $sliArrNum[1];
            $n3 = $sliArrNum[2];
            $n4 = $sliArrNum[3];
            $leftTime = floor($arrBus['MsgBody']['ArriveInfoList']['row'][$i]["PREDICT_TRAV_TM"]/60);
            //기존 남은 시간을 분단위로 제공하던 api가 초단위로 변경됨.// floor>소수점 이하를 버려주는 함수
            //$hyp = "-"; 따로 변수 지정하지 않아도 가능.
            
            if($arrBus['MsgBody']['ArriveInfoList']['row'][$i]['ARRV_VH_ID'] == 0){//아직 오지 않는(도착 차량 정보가 없는) 버스를 걸러줌.
                continue;
            }elseif(($n1 == 0)&&($n4 == 0)){
                $busNum = $n2.$n3;
            }elseif(($n1 == 0)&&($n4 != 0)){
                $busNum = $n2.$n3."-".$n4;
            }elseif(($n1 != 0)&&($n4 != 0)){
                $busNum = $n1.$n2.$n3."-".$n4;
            }else{
                $busNum = $n1.$n2.$n3;
            }
            
            //$totalString = $totalString.$busNum. " 번 버스는 " . $arrBus['MsgBody']['ArriveInfoList']['row'][$i]["LEFT_STATION"]. " 정거장 전에 있으며 도착 예정시간은 약 " . $arrBus['MsgBody']['ArriveInfoList']['row'][$i]["PREDICT_TRAV_TM"]. " 분 후 입니다. \n";
            $totalString = $totalString.$busNum. " 번 버스는 " . $arrBus['MsgBody']['ArriveInfoList']['row'][$i]["LEFT_STATION"]. " 정거장 전에 있으며 도착 예정시간은 약 " . $leftTime. " 분 후 입니다. \n";
            //9자리 숫자로 이루어진 ROUTE_ID 에서 필요한 만큼(버스번호)만 빼기위해 값을 정리해 $busNum에 삽입후 결과를 묶어 출력.
        }
    }elseif($getSta == null){
        echo "돌아가 정류장을 선택해 주세요!";
    }else{
        $num2 = $_GET['busNo'];
        $arrNum = str_split($num2);
        $sliArrNum = array_slice($arrNum, 5);
        $n1 = $sliArrNum[0];
        $n2 = $sliArrNum[1];
        $n3 = $sliArrNum[2];
        $n4 = $sliArrNum[3];
        $leftTime = floor($arrBus['MsgBody']['ArriveInfoList']['row']["PREDICT_TRAV_TM"]/60);
        //$hyp = "-"; 따로 변수 지정하지 않아도 가능.
        if($_GET['busNo'] != $arrBus['MsgBody']['ArriveInfoList']['row']["ROUTE_ID"]){
            echo "이 버스는 이곳에 정차하지 않습니다.";
            return;
        }elseif($arrBus['MsgBody']['ArriveInfoList']['row']['ARRV_VH_ID'] == 0){
            echo "현재 오고있는 버스가 없습니다.";
            return;
        }elseif(($n1 == 0)&&($n4 == 0)){
            $busNm = $n2.$n3;//동작.
        }elseif(($n1 == 0)&&($n4 != 0)){
            $busNm = $n2.$n3."-".$n4;
        }elseif(($n1 != 0)&&($n4 != 0)){
            $busNm = $n1.$n2.$n3."-".$n4;
        }else{
            $busNm = $n1.$n2.$n3;
        }
        //$totalString = $busNm. " 번 버스는 " . $arrBus['MsgBody']['ArriveInfoList']['row']["LEFT_STATION"]. " 정거장 전에 있으며 도착 예정시간은 " . $arrBus['MsgBody']['ArriveInfoList']['row']["PREDICT_TRAV_TM"]. " 분 후 입니다. \n";
        $totalString = $busNm. " 번 버스는 " . $arrBus['MsgBody']['ArriveInfoList']['row']["LEFT_STATION"]. " 정거장 전에 있으며 도착 예정시간은 " . $leftTime. " 분 후 입니다. \n";
    }
    if(($getSta != null)&&($totalString == null)){
        echo "현재 오고있는 버스가 없습니다.";
    }
    echo $totalString;
	//도착정보의 ROUTE_ID를 노선정보의 ROUTE_NM과 짝지어줘야함.
	
	
	curl_close($ch);
	
?>
