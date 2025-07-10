# QuickLabel: 技術仕様書
1. 概要
    1.1. 目的本ドキュメントは、CUI画像ラベリングツール QuickLabel の内部設計、クラス構造、および処理フローを定義する。将来的な機能追加やメンテナンスを行う開発者が、迅速かつ正確にコードベースを理解することを目的とする。

    1.2. アーキテクチャ本ツールは、責務の分離を目的とし、MVC (Model-View-Controller) パターンに類似した以下の3クラス構造を基本アーキテクチャとして採用している。Model: DataManagerクラスが担当。ファイルI/Oに特化し、データの永続化を管理する。View: TerminalViewクラスが担当。ターミナルへの表示とユーザー入力の受付を管理する。Controller: LabelingToolクラスが担当。アプリケーション全体のロジック、状態管理、および他クラスへの指示を行う。

2. ファイル構成
ファイル名説明main.pyアプリケーションのエントリーポイント。コマンドライン引数を解析し、LabelingToolを起動する。tool.pyLabelingToolクラスを定義。アプリケーションの核となるコントローラー。data_manager.pyDataManagerクラスを定義。JSONファイルの永続化を担当するモデル。terminal_view.pyTerminalViewクラスを定義。ターミナルUIを担当するビュー。

3. クラス設計
    3.1. LabelingTool (Controller / tool.py)アプリケーション全体のロジックと状態（ステート）を管理する「司令塔」。
    責務
    - アプリケーションの起動、モードに応じた処理の振り分け。
    - ユーザーコマンドの解釈と、それに基づく内部状態の更新。
    - DataManagerへのデータ永続化の指示。
    - TerminalViewへの表示更新の指示。
    - OpenCVウィンドウの生成と管理。

    主要な属性
    属性名型説明
    self.modestr現在の操作モード (single, multi, add_label)。
    self.imageslist処理対象の全画像ファイルパスのリスト。
    self.statesdict現在の作業進捗 (last_processed_index)。
    self.annotationsdict全てのアノテーションデータ。
    self.label_listdict全てのラベルマスタデータ。
    self.current_indexint現在処理中の画像のインデックス。
    self.current_imagestr現在処理中の画像のファイル名。
    self.messagestrTerminalViewに表示する一時的なメッセージ。
    self.quit_flagboolアプリケーション終了を通知するフラグ。
    self.window_namestrOpenCVで表示するウィンドウの名前。
    
    主要なメソッド
    - __init__(self, folder, mode): 各クラスのインスタンス化、DataManagerからのデータロード、状態変数の初期化を行う。
    - run(self): メインエントリーポイント。モードに応じて_label_image()または_add_label()を呼び出す。OpenCVウィンドウの生成もここで行う。
    - _label_image(self): 画像ラベリングのメインループ。状態管理、UI表示、コマンド処理のサイクルを回す。
    - _add_label(self): ラベルマスタ編集のメインループ。
    - _process_label_command(self, command): ラベリングモードで入力されたコマンドを解釈し、_update_*メソッドを呼び出して状態を更新する。
    - _process_add_label_command(self, command): ラベル追加モードで入力されたコマンドを解釈し、状態を更新する。
    - _update_states(self, number): self.statesを更新する。
    - _update_annotation(self, label, action): self.annotationsを更新する。
    - _update_label_list(self, label, action): self.label_listを更新する。
    - _show_image(self, image_path): OpenCVを用いて指定された画像を表示する。

    3.2. DataManager (Model / data_manager.py)
    ファイルI/Oに特化した「データの番人」。自身では状態を保持しない（ステートレス）。

    責務
    - プロジェクトフォルダ内の各JSONファイル（state.json, annotations.json, labels.json）のパス管理。
    - 起動時にファイルが存在しない場合、初期内容でファイルを自動生成する。
    - LabelingToolからの指示に基づき、JSONファイルの読み込み（load_*）と書き込み（save_*）を行う。
    
    主要なメソッド
    - __init__(self, project_folder, images): 管理対象ファイルのパスを確定し、_initialize_files()を呼び出す。
    - _initialize_files(self): 各ファイルの存在を確認し、なければ空の状態で新規作成する。
    - load_* メソッド群: 対応するJSONファイルを読み込み、Pythonの辞書オブジェクトとして返す。
    - save_* メソッド群: LabelingToolから渡された辞書オブジェクトを、対応するJSONファイルに書き込む。日本語が文字化けしないようensure_ascii=Falseを指定する。
    - search_label(self, label_list, search_labels): 指定されたキーワードに部分一致するラベルを検索し、そのインデックスと名前の辞書を返す。

    3.3. TerminalView (View / terminal_view.py)
    ターミナル上の全ての入出力を担当する「表示の専門家」。
    
    責務
    - ターミナル画面のクリア。
    - LabelingToolから渡されたデータに基づき、整形されたUIをターミナルに表示する。
    - モードに応じて表示内容を切り替える。ユーザーからのキーボード入力を受け付ける。
    
    主要なメソッド
    - __init__(self): （現時点では処理なし）
    - render(self, display_data, message, mode): メインの描画メソッド。モードに応じてview_label_image()またはview_add_label()に処理を振り分ける。
    - view_label_image(self, display_data, message): ラベリングモードのUIを描画する。
    - view_add_label(self, display_data, message): ラベル追加モードのUIを描画する。
    - get_input(self, input_sentence): プロンプトを表示し、ユーザーのキーボード入力を受け付けて返す。
    - show_message(self, message): 一時的なメッセージを表示する。
    
4. 処理フローの要点
- 起動シーケンス: main.py -> LabelingTool.__init__ -> DataManager.__init__ (ファイル初期化) -> LabelingTool.run() -> _label_image() or _add_label()
- 状態管理: 全てのアプリケーション状態（現在のインデックス、アノテーションデータ等）はLabelingToolのインスタンス属性として一元管理される。DataManagerやTerminalViewは状態を持たない。
- データ永続化: ユーザーがコマンドを実行し、_process_*_commandメソッド内で状態が更新された直後、DataManagerのsave_*メソッドが呼び出され、変更が即座にファイルに書き込まれる。これにより、データ損失のリスクを最小限に抑えている。
- UI更新: メインループの各サイクルで、LabelingToolは最新の状態をdisplay_dataとしてTerminalViewに渡し、render()を呼び出すことで画面が再描画される。