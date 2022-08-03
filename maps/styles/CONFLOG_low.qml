<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" minScale="1e+08" version="3.24.1-Tisler" styleCategories="AllStyleCategories" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="0" fetchMode="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option type="bool" value="false" name="WMSBackgroundLayer"/>
      <Option type="bool" value="false" name="WMSPublishDataSourceUrl"/>
      <Option type="int" value="0" name="embeddedWidgets/count"/>
      <Option type="QString" value="Value" name="identify/format"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" value="" name="name"/>
      <Option name="properties"/>
      <Option type="QString" value="collection" name="type"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling enabled="false" maxOversampling="2" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer classificationMax="2000" band="1" nodataColor="" opacity="1" type="singlebandpseudocolor" alphaBand="-1" classificationMin="0">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader maximumValue="2000" minimumValue="0" labelPrecision="4" clip="0" colorRampType="INTERPOLATED" classificationMode="1">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option type="QString" value="68,1,84,191" name="color1"/>
              <Option type="QString" value="253,231,37,191" name="color2"/>
              <Option type="QString" value="ccw" name="direction"/>
              <Option type="QString" value="0" name="discrete"/>
              <Option type="QString" value="gradient" name="rampType"/>
              <Option type="QString" value="rgb" name="spec"/>
              <Option type="QString" value="0.0196078;70,8,92,191;rgb;ccw:0.0392157;71,16,99,191;rgb;ccw:0.0588235;72,23,105,191;rgb;ccw:0.0784314;72,29,111,191;rgb;ccw:0.0980392;72,36,117,191;rgb;ccw:0.117647;71,42,122,191;rgb;ccw:0.137255;70,48,126,191;rgb;ccw:0.156863;69,55,129,191;rgb;ccw:0.176471;67,61,132,191;rgb;ccw:0.196078;65,66,135,191;rgb;ccw:0.215686;63,72,137,191;rgb;ccw:0.235294;61,78,138,191;rgb;ccw:0.254902;58,83,139,191;rgb;ccw:0.27451;56,89,140,191;rgb;ccw:0.294118;53,94,141,191;rgb;ccw:0.313725;51,99,141,191;rgb;ccw:0.333333;49,104,142,191;rgb;ccw:0.352941;46,109,142,191;rgb;ccw:0.372549;44,113,142,191;rgb;ccw:0.392157;42,118,142,191;rgb;ccw:0.411765;41,123,142,191;rgb;ccw:0.431373;39,128,142,191;rgb;ccw:0.45098;37,132,142,191;rgb;ccw:0.470588;35,137,142,191;rgb;ccw:0.490196;33,142,141,191;rgb;ccw:0.509804;32,146,140,191;rgb;ccw:0.529412;31,151,139,191;rgb;ccw:0.54902;30,156,137,191;rgb;ccw:0.568627;31,161,136,191;rgb;ccw:0.588235;33,165,133,191;rgb;ccw:0.607843;36,170,131,191;rgb;ccw:0.627451;40,174,128,191;rgb;ccw:0.647059;46,179,124,191;rgb;ccw:0.666667;53,183,121,191;rgb;ccw:0.686275;61,188,116,191;rgb;ccw:0.705882;70,192,111,191;rgb;ccw:0.72549;80,196,106,191;rgb;ccw:0.745098;90,200,100,191;rgb;ccw:0.764706;101,203,94,191;rgb;ccw:0.784314;112,207,87,191;rgb;ccw:0.803922;124,210,80,191;rgb;ccw:0.823529;137,213,72,191;rgb;ccw:0.843137;149,216,64,191;rgb;ccw:0.862745;162,218,55,191;rgb;ccw:0.882353;176,221,47,191;rgb;ccw:0.901961;189,223,38,191;rgb;ccw:0.921569;202,225,31,191;rgb;ccw:0.941176;216,226,25,191;rgb;ccw:0.960784;229,228,25,191;rgb;ccw:0.980392;241,229,29,191;rgb;ccw" name="stops"/>
            </Option>
            <prop k="color1" v="68,1,84,191"/>
            <prop k="color2" v="253,231,37,191"/>
            <prop k="direction" v="ccw"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="spec" v="rgb"/>
            <prop k="stops" v="0.0196078;70,8,92,191;rgb;ccw:0.0392157;71,16,99,191;rgb;ccw:0.0588235;72,23,105,191;rgb;ccw:0.0784314;72,29,111,191;rgb;ccw:0.0980392;72,36,117,191;rgb;ccw:0.117647;71,42,122,191;rgb;ccw:0.137255;70,48,126,191;rgb;ccw:0.156863;69,55,129,191;rgb;ccw:0.176471;67,61,132,191;rgb;ccw:0.196078;65,66,135,191;rgb;ccw:0.215686;63,72,137,191;rgb;ccw:0.235294;61,78,138,191;rgb;ccw:0.254902;58,83,139,191;rgb;ccw:0.27451;56,89,140,191;rgb;ccw:0.294118;53,94,141,191;rgb;ccw:0.313725;51,99,141,191;rgb;ccw:0.333333;49,104,142,191;rgb;ccw:0.352941;46,109,142,191;rgb;ccw:0.372549;44,113,142,191;rgb;ccw:0.392157;42,118,142,191;rgb;ccw:0.411765;41,123,142,191;rgb;ccw:0.431373;39,128,142,191;rgb;ccw:0.45098;37,132,142,191;rgb;ccw:0.470588;35,137,142,191;rgb;ccw:0.490196;33,142,141,191;rgb;ccw:0.509804;32,146,140,191;rgb;ccw:0.529412;31,151,139,191;rgb;ccw:0.54902;30,156,137,191;rgb;ccw:0.568627;31,161,136,191;rgb;ccw:0.588235;33,165,133,191;rgb;ccw:0.607843;36,170,131,191;rgb;ccw:0.627451;40,174,128,191;rgb;ccw:0.647059;46,179,124,191;rgb;ccw:0.666667;53,183,121,191;rgb;ccw:0.686275;61,188,116,191;rgb;ccw:0.705882;70,192,111,191;rgb;ccw:0.72549;80,196,106,191;rgb;ccw:0.745098;90,200,100,191;rgb;ccw:0.764706;101,203,94,191;rgb;ccw:0.784314;112,207,87,191;rgb;ccw:0.803922;124,210,80,191;rgb;ccw:0.823529;137,213,72,191;rgb;ccw:0.843137;149,216,64,191;rgb;ccw:0.862745;162,218,55,191;rgb;ccw:0.882353;176,221,47,191;rgb;ccw:0.901961;189,223,38,191;rgb;ccw:0.921569;202,225,31,191;rgb;ccw:0.941176;216,226,25,191;rgb;ccw:0.960784;229,228,25,191;rgb;ccw:0.980392;241,229,29,191;rgb;ccw"/>
          </colorramp>
          <item label="0,0000" color="#440154" alpha="191" value="0"/>
          <item label="39,2156" color="#46085c" alpha="191" value="39.2156"/>
          <item label="78,4314" color="#471063" alpha="191" value="78.4314"/>
          <item label="117,6470" color="#481769" alpha="191" value="117.647"/>
          <item label="156,8628" color="#481d6f" alpha="191" value="156.8628"/>
          <item label="196,0784" color="#482475" alpha="191" value="196.07840000000002"/>
          <item label="235,2940" color="#472a7a" alpha="191" value="235.294"/>
          <item label="274,5100" color="#46307e" alpha="191" value="274.51"/>
          <item label="313,7260" color="#453781" alpha="191" value="313.726"/>
          <item label="352,9420" color="#433d84" alpha="191" value="352.94199999999995"/>
          <item label="392,1560" color="#414287" alpha="191" value="392.156"/>
          <item label="431,3720" color="#3f4889" alpha="191" value="431.37199999999996"/>
          <item label="470,5880" color="#3d4e8a" alpha="191" value="470.588"/>
          <item label="509,8040" color="#3a538b" alpha="191" value="509.80400000000003"/>
          <item label="549,0200" color="#38598c" alpha="191" value="549.02"/>
          <item label="588,2360" color="#355e8d" alpha="191" value="588.236"/>
          <item label="627,4500" color="#33638d" alpha="191" value="627.4499999999999"/>
          <item label="666,6660" color="#31688e" alpha="191" value="666.6659999999999"/>
          <item label="705,8820" color="#2e6d8e" alpha="191" value="705.8820000000001"/>
          <item label="745,0980" color="#2c718e" alpha="191" value="745.0980000000001"/>
          <item label="784,3140" color="#2a768e" alpha="191" value="784.314"/>
          <item label="823,5300" color="#297b8e" alpha="191" value="823.53"/>
          <item label="862,7460" color="#27808e" alpha="191" value="862.746"/>
          <item label="901,9600" color="#25848e" alpha="191" value="901.96"/>
          <item label="941,1760" color="#23898e" alpha="191" value="941.176"/>
          <item label="980,3920" color="#218e8d" alpha="191" value="980.392"/>
          <item label="1019,6080" color="#20928c" alpha="191" value="1019.6080000000001"/>
          <item label="1058,8240" color="#1f978b" alpha="191" value="1058.824"/>
          <item label="1098,0400" color="#1e9c89" alpha="191" value="1098.04"/>
          <item label="1137,2540" color="#1fa188" alpha="191" value="1137.254"/>
          <item label="1176,4700" color="#21a585" alpha="191" value="1176.4699999999998"/>
          <item label="1215,6860" color="#24aa83" alpha="191" value="1215.6860000000001"/>
          <item label="1254,9020" color="#28ae80" alpha="191" value="1254.902"/>
          <item label="1294,1180" color="#2eb37c" alpha="191" value="1294.1180000000002"/>
          <item label="1333,3340" color="#35b779" alpha="191" value="1333.334"/>
          <item label="1372,5500" color="#3dbc74" alpha="191" value="1372.55"/>
          <item label="1411,7640" color="#46c06f" alpha="191" value="1411.7640000000001"/>
          <item label="1450,9800" color="#50c46a" alpha="191" value="1450.98"/>
          <item label="1490,1960" color="#5ac864" alpha="191" value="1490.1960000000001"/>
          <item label="1529,4120" color="#65cb5e" alpha="191" value="1529.412"/>
          <item label="1568,6280" color="#70cf57" alpha="191" value="1568.628"/>
          <item label="1607,8440" color="#7cd250" alpha="191" value="1607.844"/>
          <item label="1647,0580" color="#89d548" alpha="191" value="1647.058"/>
          <item label="1686,2740" color="#95d840" alpha="191" value="1686.2740000000001"/>
          <item label="1725,4900" color="#a2da37" alpha="191" value="1725.49"/>
          <item label="1764,7060" color="#b0dd2f" alpha="191" value="1764.7060000000001"/>
          <item label="1803,9220" color="#bddf26" alpha="191" value="1803.922"/>
          <item label="1843,1380" color="#cae11f" alpha="191" value="1843.138"/>
          <item label="1882,3520" color="#d8e219" alpha="191" value="1882.352"/>
          <item label="1921,5680" color="#e5e419" alpha="191" value="1921.568"/>
          <item label="1960,7840" color="#f1e51d" alpha="191" value="1960.784"/>
          <item label="2000,0000" color="#fde725" alpha="191" value="2000"/>
          <rampLegendSettings useContinuousLegend="1" maximumLabel="" suffix="" prefix="" direction="0" orientation="1" minimumLabel="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="QChar" value="" name="decimal_separator"/>
                <Option type="int" value="6" name="decimals"/>
                <Option type="int" value="0" name="rounding_type"/>
                <Option type="bool" value="false" name="show_plus"/>
                <Option type="bool" value="true" name="show_thousand_separator"/>
                <Option type="bool" value="false" name="show_trailing_zeros"/>
                <Option type="QChar" value="" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0" gamma="1"/>
    <huesaturation grayscaleMode="0" invertColors="0" colorizeOn="0" colorizeRed="255" colorizeGreen="128" colorizeStrength="100" colorizeBlue="128" saturation="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
