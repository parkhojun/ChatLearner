var express = require("express"),
  cors = require("cors");
  
const { spawn } = require('child_process');

var app = express();
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cors({
  origin: 'https://ainize.ai',
}));

var repo_dir = '.';

app.get('/chatbot', async (req, res) => {
  console.log('get /chatbot')
  const sentence = req.query.sentence
  console.log(req)
  console.log(sentence)
  ret = await runPython(sentence)
  res.json(ret)
})

app.listen(80, () => {
  console.log("server connect");
});

//run python except densepose
runPython = (sentence) => {
  return new Promise((resolve, reject) => {
    let ret = ''
    let config = [
      repo_dir + "/chatbot/botui.py", "sentence", '"'+sentence+'"',
    ]// botui.py se- --model model --input input
    const pyProg = spawn('python3', config)
    
    pyProg.stderr.on('data', (data) => {
      console.log("runpython return error : " + data.toString())
      resolve(data.toString())
    })

    pyProg.stdout.on('data', (data) =>
      ret += data
    )
    
    pyProg.on('exit', (code) =>{
      console.log('exit code : ' + code)
      resolve(JSON.stringify(ret))
    })
  })
};