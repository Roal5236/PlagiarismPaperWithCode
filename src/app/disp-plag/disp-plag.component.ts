import { Component, OnInit, OnDestroy } from '@angular/core';
import { PostsService } from 'src/app/posts.service';
import { Subscription } from 'rxjs';
@Component({
  selector: 'app-disp-plag',
  templateUrl: './disp-plag.component.html',
  styleUrls: ['./disp-plag.component.css']
})
export class DispPlagComponent implements OnInit, OnDestroy {
  // tslint:disable: no-string-literal

  posts: any;
  DocsPerc: any;
  docPlag: any;
  userSentences: any;
  displaySpinner: any;
  private postSub: Subscription;
  private SpinnerSub: Subscription;
  private PanelSub: Subscription;
  panelId: any;
  plagPerc = null;

  constructor(public postsService: PostsService) {
  }

  disp() {
    if (this.userSentences != null) {
      return 'block';
    } else {
      return 'none';
    }
  }

  displaySpinnerFunct() {
    if (this.displaySpinner === 'block') {
        return 'block';
     }
    return 'none';
  }

  ngOnInit() {
    this.postSub = this.postsService.getPostsUpdatedListner()
      .subscribe((posts: any) => {

        if(posts != null){
          this.plagPerc = posts['perc'];
          this.docPlag =  Object.keys(posts['DocsPerc']).length;
          this.DocsPerc = posts['DocsPerc'];
          this.userSentences = posts['userSentences'];
          console.log('disp-page sentences', this.userSentences);
        } else{
          console.log('disp-page sentences', posts);
        }

    });

    this.SpinnerSub = this.postsService.displaySpinnerListner().subscribe((displaySpinner) => {
      this.displaySpinner = displaySpinner;
    });

    this.PanelSub = this.postsService.OpenPanelListner().subscribe((panelId) => {
      console.log('Open This Panel:', panelId);
      this.panelId = panelId;
    });

  }

  ngOnDestroy(){
    this.postSub.unsubscribe();
    this.SpinnerSub.unsubscribe();
    this.PanelSub.unsubscribe();
  }

}
