import { Component, OnInit, OnDestroy, Injectable, ViewEncapsulation   } from '@angular/core';
import { PostsService } from 'src/app/posts.service';
import {HttpClient } from '@angular/common/http';
import { Subscription } from 'rxjs';


@Component({
  selector: 'app-plag-page',
  templateUrl: './plag-page.component.html',
  styleUrls: ['./plag-page.component.css'],
})
@Injectable()
export class PlagPageComponent implements OnInit, OnDestroy {
  // tslint:disable: no-string-literal
  // tslint:disable: one-line



  constructor(public postsService: PostsService, private http: HttpClient) { }

  UserText;
  posts: object;
  userSentences=null;
  private postSub: Subscription;
  private fileSub: Subscription;
  htmltoDisplay='';
  selectedFile: File = null;
  UploadFileText = 'Select File';


  changeColor(UploadFileText){
    if (UploadFileText === 'Select File') {
      return '#0066cc';
     }
    return '#00b359';
  }

  displayBar(UploadFileText){
    if (UploadFileText === 'Select File') { return 'none'; }
    else if (UploadFileText === 'Uploaded') { return 'none'; }
    else{ return 'block'; }

  }

  ngOnInit() {
    this.posts = this.postsService.getPosts();
    this.postSub = this.postsService.getPostsUpdatedListner()
      .subscribe((posts: any) => {
        if(posts != null){
          this.userSentences = posts['userSentences'];
          console.log('plag-page sentences', this.userSentences);
        } else{
          console.log('plag-page sentences', posts);
        }
      });

    // This is a subscribtion for Upload File Button
    this.postSub = this.postsService.fileUploadedListner()
      .subscribe((fileName: any) => {
        console.log('filename: ', fileName);
        this.UploadFileText = fileName;
      });
  }

  ngOnDestroy(){
    this.postSub.unsubscribe();
  }

  getEditorText(){
      const text = document.getElementById('editor').textContent;
      if(text.length > 0) {
        this.postsService.send_post(text);
      } else {

      }
  }

  disp(){
    if(this.userSentences === null){
      return 'block';
    } else{

      return 'none';
    }
  }

  hide(){
    if(this.userSentences !== null){
      return 'block';
    } else{

      return 'none';
    }
  }

  switchEditor(){
    this.userSentences=null;
    document.getElementById('editor').innerHTML = document.getElementById('textafter').innerHTML;
  }

}
