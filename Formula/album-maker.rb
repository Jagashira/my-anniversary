class AlbumMaker < Formula
  desc "Anniversary Album Maker – PDF photo album generator"
  homepage "https://github.com/Jagashira/my-anniversary"
  url "https://github.com/Jagashira/my-anniversary/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "157b23d0e0ed827f4f786608d2e41a3489b2983fa05903aaf2a40e1f2b36075d"
  license "MIT"

  depends_on "python@3.12"
  depends_on "pyqt@6"

  def install
    bin.install "gui.py" => "album-maker"
    prefix.install Dir["*"]
  end

  test do
    system "#{bin}/album-maker", "--version"
  end
end
