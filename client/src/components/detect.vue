<template>
    <div>
      <video ref="videoElement"  width="200" height="200"></video>
      <button @click="startHandTracking">开始手势识别</button>
    </div>
</template>
<script>
import * as handTrack from 'handtrackjs';
export default {
    
  props: {
  },
  data(){
    return{
        head_x:1.0,   //头部x坐标
        hand_x:1.0,   //左手x坐标
        center_x:50,
    }

  },
  methods: {
  async startHandTracking() {
    const videoElement = this.$refs.videoElement;
  const modelParams = {
    flipHorizontal: true, // 镜像翻转
    maxNumBoxes: 3, // 最大检测框数量
    iouThreshold: 0.5, // IOU阈值
    scoreThreshold: 0.5, // 置信度阈值
  };

  // 初始化手势识别器
  handTrack.load(modelParams).then((model) => {
    // 开始识别手势
    handTrack.startVideo(videoElement).then((status) => {
      if (status) {
        console.log('手势识别已启动');
        this.$refs.videoElement.style.width='400px';
        this.$refs.videoElement.style.height='400px'
        // 开始检测手势
        this.detectHandGesture(model);
      } else {
        console.log('无法启动手势识别');
      }
    });
  });
    
  },
  detectHandGesture(model) {
  const videoElement = this.$refs.videoElement;
  // 持续检测手势
  setInterval(() => {
    model.detect(videoElement).then((predictions) => {
      if (predictions.length > 0) {
        // 识别到手势
        const handGesture = predictions[0];
        //console.log(predictions)
        this.getPosition(handGesture);   //更新头或手坐标
        //console.log('识别结果:', handGesture);
        this.moveline(handGesture.label);   //移动折线图
      }
    });
  }, 100); // 每100毫秒检测一次
},
//获取左手,头和右手的位置
getPosition(res){
    if(res.label=="face")this.head_x=(res.bbox[0]+res.bbox[2])/2;
    else this.hand_x=(res.bbox[0]+res.bbox[2])/2;
},
//根据手势移动情况进行缩放
moveline(label){
    if(this.head_x==0.0||this.hand_x==0.0)return  //假如0.0,则不动
    //console.log(this.hand_x)
    if(this.center_x<this.hand_x){  //右手
        if(label=='open')this.$emit('right_event', { message: 'large' });  //扩大
        else this.$emit('right_event', { message: 'small' });  //缩小 
    }
    if(this.center_x>this.hand_x){  //左手
        if(label=='open')this.$emit('left_event', { message: 'large' });  //扩大
        else this.$emit('left_event', { message: 'small' });  //扩大
    }
}

}


}
</script>
<style>
.advice {
  border: 1px solid #ccc;
  padding: 10px;
  margin-top: 20px;
}
</style>
