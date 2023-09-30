# LearningPathGenerator

[![badge](https://img.shields.io/badge/license-MIT-blue)](https://github.com/DavidZhang0710/Params2json/blob/main/LICENSE)

A python project to generate a learning path on a specific topic or question. Using the LLMs API and MPNet model to automatically create a learning path chart for a question in 'HOW TO ... ?' form.

## Project Introduction
Nowadays, more and more LLMs are trained to deal various kinds of problems, like ***Recommendation System*** or ***text translation***, but we can see that most of these model work badlly with the ***deep-logical-chain*** task, 

## Project Requirement
Python 3



## Quick Start

1. Download this repo and required python modules

   ```bash
   git clone https://github.com/DavidZhang0710/LearningPathGenerator.git
   cd ./LearningPathGenerator
   pip install -r requirements.txt
   ```

2. Download MPNet model

   The default MPNet model is [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2), which can be downloaded form huggingface and loaded by a python module named ***SentenceTransformer***.

   ```bash
   cd ./LearningPathGenerator
   git submodule update --init --recursive
   ```

   And if you want to use other SentenceTransformer, you can download it and replace the code fragment below in LearningPathGenerator/Estimate.py.

   ```python
   def estimate(reference_text,pool_list):
       model = SentenceTransformer('path/to/your/model')
   ```

   But make sure that can be identified by *SentenceTransformer()*.

3. Apply LLMs API (or local model)
   
   The LLMs API used in this project is ***ERNIE Bot*** developed by Baidu, you can surface their website to get an API_KEY along with an SECRET_KEY, which will be used later.
   
   After you finished the step 1, you can find *LearningPathGenerator/config.json*, you are supposed to replace the values of "API_KEY" and "SECRET_KEY" with those you have got.
   
   E.g.
   
   ```json
   {
       "API_KEY" : "YOUR_API_KEY",
       "SECRET_KEY" : "YOUR_SECRET_KEY"
   }
   ```
   
   Similarly, if you want to use other LLMs API, you can adapt the ***get_answer()*** in *LearningPathGenerator/getAnswer.py* to your own version, but remember that you should keep the input and output form same with the original version.

4. Demo

   If you want to experience a small demo of this project, you can click ***[here](http://124.221.34.139/projects/pathgenerator.html)*** to turn to a web demo.

## More Details

#### 模块定义方法

```c++
namespace params2json {
    //T类型转json
    template <typename T>
		Json::Value toJson(const T& value);
    //定义与函数相对应的结构体funcname_s，放在头文件（.h）中
    STRUCT_WITH_XMEMBER(funcname, typename_0, paramname_0,...)
    //对于上述结构体toJson的实现，放在实现（.cc）中
    IMPL_STRUCT_WITH_XMEMBER(funcname, typename_0, paramname_0,...)
    //和上述结构体配合，生成入参的json字符串
    template <typename T>
    std::string make_message(const T& t);
}
```



- #### 添加函数宏

  对于函数`void func (typename_0, param_0, typename_1, param_1)`，只需要进行如下的宏定义

  ```c++
  STRUCT_WITH_XMEMBER(func, typename_0, param_0, typename_1, param_1)
  IMPL_STRUCT_WITH_XMEMBER(func, typename_0, param_0, typename_1, param_1)
  ```

  然后就可以使用宏定义所定义的结构体func_s和make_message生成需要的json字符串

  ```c++
  std::string json_str = params2json::make_message(params2json::func_s(param_0, param_1));
  ```

  

- #### 添加自定义序列化函数toJson()

  对于简单类型，已经存在toJson()的定义，也可以通过如下方式进行特化，以输出想要的json格式：

  ```c++
  template <>
  Json::Value toJson<bool>(const bool& value) {
      if (value)  return Json::Value("True");
      return Json::Value("False");
  }
  ```

  对于复杂类型，例如结构体或类，需要手动定义toJson（因为成员名信息在编译时已丢失，非侵入式不得不手动编写）具体如下：

  ```c++
  struct simple {
      int num;
      bool flag;
  };
  
  struct complex {
      int num;
      simple struct_member;
  };
  
  template<>
  Json::Value toJson<simple>(const simple& obj) {
      Json::Value value;
      value["num"] = toJson(obj.num);
      value["flag"] = toJson(obj.flag);
      return value;
  }
  
  template<>
  Json::Value toJson<complex>(const complex& obj) {
      Json::Value value;
      value["num"] = toJson(obj.num);
      value["struct_member"] = toJson(obj.struct_member);
      return value;
  }
  ```

  更多细节可以查看`src\example.cpp`

- #### 添加自定义make_message()

  `make_message()`是基于`Json::StreamWriter`编写的将`Json::Value`对象转换为字符串输出的方法，如果需要更加自定义的方式，可以重载`make_message()`。
  
  也可以通过`toJson(func_s())`的方式直接获取由入参的 `Json::Value`对象，并通过自定义的方式进行处理。

  
